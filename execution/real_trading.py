from execution.broker_api import BrokerAPI
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("execution.live")

class LiveTradingEngine(BrokerAPI):
    """
    Connects to Alpaca's Live Trading environment.
    DANGEROUS: Executes real money trades.
    """
    def __init__(self):
        # Force the live URL
        base_url = "https://api.alpaca.markets"
        api_key = Config.ALPACA_API_KEY
        secret_key = Config.ALPACA_SECRET_KEY
        
        if not api_key or not secret_key:
            logger.error("LIVE TRADING BLOCKED: Alpaca API keys are missing from the environment.")
            
        super().__init__(api_key=api_key, secret_key=secret_key, base_url=base_url)
        
    def place_order(self, symbol: str, qty: float, side: str, order_type: str = 'market', time_in_force: str = 'day') -> dict:
        if not self.api_key:
            return {"error": "Missing LIVE API keys. Real trade blocked."}
            
        logger.warning(f"!!! EXECUTING LIVE {side.upper()} TRADE FOR {qty} {symbol} !!!")
        return super().place_order(symbol, qty, side, order_type, time_in_force)
