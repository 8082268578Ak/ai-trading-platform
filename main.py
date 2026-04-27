import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import concurrent.futures

from config.settings import Config
from utils.logger import get_logger
from data.fetcher import DataFetcher
from data.processing import FeatureEngineer
from sentiment.analyzer import SentimentAnalyzer
from models.lstm_model import LSTMPricePredictor
from models.rf_model import RandomForestPredictor
from models.xgb_model import XGBoostPredictor
from strategy.engine import StrategyEngine
from backtesting.runner import BacktestRunner
from portfolio.risk import RiskAnalyzer
from portfolio.optimizer import PortfolioOptimizer

logger = get_logger("main")

def process_single_ticker(ticker=Config.DEFAULT_TICKER, model_type="lstm", start_date=Config.DATA_START_DATE):
    logger.info(f"Starting AI Trading Pipeline for {ticker} using {model_type} model.")
    
    try:
        # 1. Fetch Data
        fetcher = DataFetcher(ticker)
        df_raw = fetcher.fetch_historical_data(start_date=start_date)
        if df_raw.empty:
            logger.error(f"No data fetched for {ticker}. Exiting.")
            return None
            
        # Calculate Risk early
        annualized_risk = RiskAnalyzer.calculate_annualized_risk(df_raw)
        risk_category = RiskAnalyzer.categorize_risk(annualized_risk)
            
        # 2. Feature Engineering
        df_processed = FeatureEngineer.add_technical_indicators(df_raw)
        FeatureEngineer.save_processed_data(df_processed, ticker)
        
        # 3. Sentiment Analysis
        sentiment_analyzer = SentimentAnalyzer()
        df_sentiment = sentiment_analyzer.get_daily_sentiment(ticker, days_back=365)
        sentiment_analyzer.save_sentiment(df_sentiment, ticker)
        
        # Merge sentiment
        if not df_sentiment.empty:
            df_merged = df_processed.join(df_sentiment, how='left')
            df_merged['Sentiment_Score'].fillna(0.0, inplace=True)
        else:
            df_merged = df_processed.copy()
            df_merged['Sentiment_Score'] = 0.0
            
        df_merged.dropna(inplace=True)
        
        # 4. Machine Learning
        if model_type == "lstm":
            model = LSTMPricePredictor()
            target_col = 'Close'
            X_train, X_test, y_train, y_test = model.prepare_data(df_merged, target_col=target_col)
            model.train(X_train, y_train, X_test, y_test)
            model.save()
            
            data_values = df_merged.values
            scaled_data = model.scaler_X.transform(data_values)
            X_all = []
            for i in range(model.seq_length, len(scaled_data)):
                X_all.append(scaled_data[i-model.seq_length:i, :])
            X_all = np.array(X_all)
            
            if len(X_all) > 0:
                predictions = model.predict(X_all)
                pred_series = [np.nan] * model.seq_length + list(predictions.flatten())
                df_merged['Predicted_Price'] = pred_series
                
        else:
            if model_type == "rf":
                model = RandomForestPredictor()
            elif model_type == "xgb":
                model = XGBoostPredictor()
                
            target_col = 'Target_Return'
            X_train, X_test, y_train, y_test = model.prepare_data(df_merged, target_col=target_col)
            model.train(X_train, y_train, X_test, y_test)
            model.save()
            
            X_all = df_merged.drop(columns=[target_col, 'Target_Class', 'Next_Close'], errors='ignore')
            X_all_scaled = model.scaler_X.transform(X_all)
            predictions_return = model.predict(X_all_scaled)
            
            df_merged['Predicted_Return'] = predictions_return
            df_merged['Predicted_Price'] = df_merged['Close'] * (1 + df_merged['Predicted_Return'])
            
        df_merged.dropna(inplace=True)
        
        # 5. Strategy
        df_signals = StrategyEngine.generate_signals(df_merged, predicted_col='Predicted_Price', sentiment_col='Sentiment_Score')
        
        # Save final dataset for dashboard
        output_path = os.path.join(Config.DATA_DIR, f"{ticker}_final_signals.csv")
        df_signals.to_csv(output_path)
        logger.info(f"Saved final signals to {output_path}")
        
        # 6. Backtesting
        metrics = BacktestRunner.run(df_signals, plot=False)
        logger.info(f"Pipeline execution completed for {ticker}.")
        
        # Return summary dict for portfolio ranking
        last_row = df_signals.iloc[-1]
        current_price = float(last_row.get('Close', 0.0))
        predicted_price = float(last_row.get('Predicted_Price', 0.0))
        sentiment = float(last_row.get('Sentiment_Score', 0.0))
        signal = last_row.get('Signal_Text', "HOLD")
        confidence = float(last_row.get('Confidence', 0.0))
        
        expected_return = 0.0
        if current_price > 0:
            expected_return = ((predicted_price - current_price) / current_price) * 100
            
        return {
            "Symbol": ticker,
            "Price": round(current_price, 2),
            "Predicted_Price": round(predicted_price, 2),
            "Expected_Return_%": round(expected_return, 2),
            "Sentiment": round(sentiment, 2),
            "Signal": signal,
            "Confidence": round(confidence, 2),
            "Annualized_Risk": round(annualized_risk, 4),
            "Risk_Category": risk_category
        }
    except Exception as e:
        logger.error(f"Error processing {ticker}: {str(e)}")
        return None

def run_multi_asset_pipeline(tickers, model_type="lstm", start_date=Config.DATA_START_DATE):
    logger.info(f"Starting Multi-Asset Pipeline for: {tickers}")
    results = []
    
    # Process sequentially to prevent Segmentation Faults from PyTorch/TensorFlow threading on Mac
    for ticker in tickers:
        try:
            logger.info(f"--- Processing {ticker} ---")
            result = process_single_ticker(ticker, model_type, start_date)
            if result:
                results.append(result)
        except Exception as exc:
            logger.error(f"{ticker} generated an exception: {exc}")
                
    if results:
        df_summary = pd.DataFrame(results)
        
        # Allocate Capital using Portfolio Optimizer
        df_summary, metadata = PortfolioOptimizer.allocate_capital(df_summary)
        
        # Sort by Allocation and Confidence descending
        df_summary = df_summary.sort_values(by=["Allocation_%", "Confidence"], ascending=[False, False])
        
        output_path = os.path.join(Config.DATA_DIR, "portfolio_summary.csv")
        df_summary.to_csv(output_path, index=False)
        logger.info(f"Saved portfolio summary to {output_path}")
        return df_summary
    return pd.DataFrame()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Multi-Asset AI Trading Pipeline")
    parser.add_argument("--tickers", type=str, default=",".join(Config.DEFAULT_TICKERS), help="Comma-separated list of stock ticker symbols")
    parser.add_argument("--model", type=str, choices=['lstm', 'rf', 'xgb'], default='lstm', help="ML model to use")
    
    args = parser.parse_args()
    tickers_list = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    
    run_multi_asset_pipeline(tickers=tickers_list, model_type=args.model)
