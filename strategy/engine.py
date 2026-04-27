import pandas as pd
from config.settings import Config
from utils.logger import get_logger
from strategy.ai_decision import generate_ai_decision

logger = get_logger("strategy.engine")

class StrategyEngine:
    """Generates trading signals based on model predictions and sentiment."""
    
    @staticmethod
    def generate_signals(df: pd.DataFrame, predicted_col: str, sentiment_col: str = 'Sentiment_Score') -> pd.DataFrame:
        """
        Generate BUY/SELL/HOLD signals using the AI Decision Engine.
        """
        logger.info("Generating trading signals using AI Decision Engine...")
        
        # Ensure columns exist
        if predicted_col not in df.columns:
            logger.error(f"Predicted column '{predicted_col}' not found.")
            df['Signal'] = 0
            return df
            
        if sentiment_col not in df.columns:
            logger.warning(f"Sentiment column '{sentiment_col}' not found. Defaulting to 0.")
            df[sentiment_col] = 0.0
            
        int_signals = []
        signal_texts = []
        confidences = []
        reasons = []
        risk_levels = []
        
        for idx, row in df.iterrows():
            decision = generate_ai_decision(row, predicted_col, sentiment_col)
            
            int_signals.append(decision['int_signal'])
            signal_texts.append(decision['signal_text'])
            confidences.append(decision['confidence'])
            reasons.append(decision['reason'])
            risk_levels.append(decision['risk_level'])
            
        df['Signal'] = int_signals
        df['Signal_Text'] = signal_texts
        df['Confidence'] = confidences
        df['Explanation'] = reasons
        df['Risk_Level'] = risk_levels
        
        logger.info(f"Generated {int_signals.count(1)} BUY, {int_signals.count(-1)} SELL signals.")
        return df
