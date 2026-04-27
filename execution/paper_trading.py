from execution.broker_api import BrokerAPI
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("execution.paper")

class PaperTradingEngine(BrokerAPI):
    """
    Connects to Alpaca's Paper Trading environment.
    Safe for simulated trades.
    """
    def __init__(self):
        # Force the paper URL
        base_url = "https://paper-api.alpaca.markets"
        api_key = Config.ALPACA_API_KEY
        secret_key = Config.ALPACA_SECRET_KEY
        
        if not api_key or not secret_key:
            logger.warning("Alpaca API keys not found in environment. Paper trading will be MOCKED locally.")
            
        super().__init__(api_key=api_key, secret_key=secret_key, base_url=base_url)
        
    def get_account_balance(self) -> dict:
        if not self.api_key:
            return {"cash": 100000.0, "portfolio_value": 100000.0, "buying_power": 100000.0, "currency": "USD", "mocked": True}
        return super().get_account_balance()
        
    def get_positions(self) -> list:
        if not self.api_key:
            return []
        return super().get_positions()

    def place_order(self, symbol: str, qty: float, side: str, order_type: str = 'market', time_in_force: str = 'day') -> dict:
        if not self.api_key:
            logger.info(f"[MOCK PAPER TRADE] Executed {side} for {qty} {symbol}.")
            return {"id": "mock-1234", "status": "accepted", "symbol": symbol, "qty": qty, "side": side}
            
        return super().place_order(symbol, qty, side, order_type, time_in_force)
