import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("data.fetcher")

class DataFetcher:
    """Class to handle downloading historical market data."""
    
    def __init__(self, ticker: str = Config.DEFAULT_TICKER):
        self.ticker = ticker
        
    def fetch_historical_data(self, start_date: str = Config.DATA_START_DATE, end_date: str = None) -> pd.DataFrame:
        """
        Fetch historical daily data for the ticker from Yahoo Finance.
        """
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
            
        logger.info(f"Fetching data for {self.ticker} from {start_date} to {end_date}")
        try:
            df = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
            
            if df.empty:
                logger.warning(f"No data fetched for {self.ticker}.")
                return df
                
            # yfinance sometimes returns MultiIndex columns if not careful, ensure single index
            if isinstance(df.columns, pd.MultiIndex):
                # Flatten the MultiIndex and keep only the metric name
                df.columns = [col[0] for col in df.columns]
                
            df.dropna(inplace=True)
            logger.info(f"Successfully fetched {len(df)} rows of data.")
            
            # Save the raw data
            self.save_data(df, "raw")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {self.ticker}: {str(e)}")
            raise
            
    def save_data(self, df: pd.DataFrame, suffix: str):
        """Save dataframe to CSV."""
        filename = f"{self.ticker}_{suffix}.csv"
        filepath = os.path.join(Config.DATA_DIR, filename)
        df.to_csv(filepath)
        logger.info(f"Saved {suffix} data to {filepath}")
        
    def load_data(self, suffix: str) -> pd.DataFrame:
        """Load dataframe from CSV."""
        filename = f"{self.ticker}_{suffix}.csv"
        filepath = os.path.join(Config.DATA_DIR, filename)
        if os.path.exists(filepath):
            logger.info(f"Loading data from {filepath}")
            # Ensure the index is DatetimeIndex
            df = pd.read_csv(filepath, index_col=0, parse_dates=True)
            return df
        else:
            logger.warning(f"File {filepath} does not exist.")
            return pd.DataFrame()
