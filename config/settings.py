import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "c9f3ca59765249cdbe7e2eab1657ffed")
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
    
    # Execution Settings
    MAX_TRADE_SIZE_USD = 5000.0
    DAILY_LOSS_LIMIT_USD = 1000.0
    
    # Data Settings
    DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT"]
    DEFAULT_TICKER = "AAPL" # Keep for fallback compatibility
    DATA_START_DATE = "2020-01-01"
    DATA_END_DATE = None # Default to today
    
    # Model Settings
    SEQ_LENGTH = 60      # Number of days to look back for LSTM
    TEST_SIZE = 0.2      # Train/Test split ratio
    BATCH_SIZE = 32
    EPOCHS = 50
    
    # Strategy Settings
    BUY_THRESHOLD = 0.5  # Example threshold for sentiment or normalized predicted return
    SELL_THRESHOLD = -0.5
    STOP_LOSS = 0.05     # 5% stop loss
    TAKE_PROFIT = 0.10   # 10% take profit
    INITIAL_CASH = 100000.0
    
    # Sentiment Settings
    SENTIMENT_MODEL = "finbert" # "finbert", "vader", or "textblob"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, "models", "saved_models")
    DATA_DIR = os.path.join(BASE_DIR, "data", "saved_data")
    
    @classmethod
    def setup_dirs(cls):
        os.makedirs(cls.MODEL_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)

# Ensure directories exist
Config.setup_dirs()
