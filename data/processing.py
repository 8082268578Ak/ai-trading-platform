import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.utils import dropna
from utils.logger import get_logger
from config.settings import Config
import os

logger = get_logger("data.processing")

class FeatureEngineer:
    """Class to handle feature engineering for stock data."""
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators using the 'ta' library.
        Includes Moving Averages, RSI, MACD, Bollinger Bands, and Volume indicators.
        """
        logger.info("Adding technical indicators...")
        try:
            # Drop NaN values just in case
            df = dropna(df)
            
            # The 'ta' library expects certain column names
            # Ensure columns are properly capitalized
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                # Try title casing if they are lowercase
                df.rename(columns={col.lower(): col.capitalize() for col in required_cols}, inplace=True)
                
            # Add all ta features
            # This adds ~86 features including momentum, volume, volatility, trend, and others
            df = add_all_ta_features(
                df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True
            )
            
            # Additional Custom Features
            # 1. Target Variable: Next day's return (1 if up, 0 if down) - for Classification
            # Or actual return for Regression
            df['Next_Close'] = df['Close'].shift(-1)
            df['Target_Return'] = (df['Next_Close'] - df['Close']) / df['Close']
            df['Target_Class'] = np.where(df['Target_Return'] > 0, 1, 0)
            
            # Drop the last row as it won't have a next close
            df.dropna(inplace=True)
            
            logger.info(f"Successfully added technical indicators. Total columns: {len(df.columns)}")
            return df
            
        except Exception as e:
            logger.error(f"Error adding technical indicators: {str(e)}")
            raise

    @staticmethod
    def save_processed_data(df: pd.DataFrame, ticker: str):
        filepath = os.path.join(Config.DATA_DIR, f"{ticker}_processed.csv")
        df.to_csv(filepath)
        logger.info(f"Saved processed data to {filepath}")
        
    @staticmethod
    def load_processed_data(ticker: str) -> pd.DataFrame:
        filepath = os.path.join(Config.DATA_DIR, f"{ticker}_processed.csv")
        if os.path.exists(filepath):
            logger.info(f"Loading processed data from {filepath}")
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        else:
            logger.warning(f"Processed file {filepath} not found.")
            return pd.DataFrame()
