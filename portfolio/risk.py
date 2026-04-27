import pandas as pd
import numpy as np
from utils.logger import get_logger

logger = get_logger("portfolio.risk")

class RiskAnalyzer:
    @staticmethod
    def calculate_annualized_risk(df: pd.DataFrame) -> float:
        """
        Calculates annualized historical volatility (risk).
        Uses daily returns pct_change.
        """
        if df.empty or 'Close' not in df.columns or len(df) < 2:
            return 0.0
            
        # Calculate daily returns
        daily_returns = df['Close'].pct_change().dropna()
        
        if daily_returns.empty:
            return 0.0
            
        # Calculate standard deviation
        std_dev = daily_returns.std()
        
        # Annualize (assuming 252 trading days)
        annualized_volatility = std_dev * np.sqrt(252)
        
        return annualized_volatility

    @staticmethod
    def categorize_risk(annualized_risk: float) -> str:
        """Categorize risk based on volatility thresholds."""
        if annualized_risk <= 0.0:
            return "Unknown"
        elif annualized_risk < 0.20:
            return "Low"
        elif annualized_risk < 0.40:
            return "Medium"
        else:
            return "High"
