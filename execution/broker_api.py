import requests
import json
from typing import Dict, Any, List
from utils.logger import get_logger
from config.settings import Config

logger = get_logger("execution.broker")

class BrokerAPI:
    """Base class for broker API integrations using Alpaca."""
    
    def __init__(self, api_key: str, secret_key: str, base_url: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key,
            "accept": "application/json"
        }
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Wrapper for making HTTP requests to the broker."""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            if response.status_code not in (200, 201, 204):
                logger.error(f"Broker API Error: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
            return response.json() if response.content else {}
            
        except Exception as e:
            logger.error(f"Failed to connect to Broker API: {str(e)}")
            return {"error": str(e)}

    def get_account_balance(self) -> Dict[str, Any]:
        """Fetch current account balance and buying power."""
        res = self._make_request('GET', 'v2/account')
        if "error" in res:
            return {"cash": 0.0, "portfolio_value": 0.0, "buying_power": 0.0}
        
        return {
            "cash": float(res.get("cash", 0.0)),
            "portfolio_value": float(res.get("portfolio_value", 0.0)),
            "buying_power": float(res.get("buying_power", 0.0)),
            "currency": res.get("currency", "USD")
        }
        
    def get_positions(self) -> List[Dict[str, Any]]:
        """Fetch all open positions."""
        res = self._make_request('GET', 'v2/positions')
        if isinstance(res, dict) and "error" in res:
            return []
        
        positions = []
        for pos in res:
            positions.append({
                "symbol": pos.get("symbol"),
                "qty": float(pos.get("qty", 0.0)),
                "market_value": float(pos.get("market_value", 0.0)),
                "unrealized_pl": float(pos.get("unrealized_pl", 0.0)),
                "current_price": float(pos.get("current_price", 0.0))
            })
        return positions

    def place_order(self, symbol: str, qty: float, side: str, order_type: str = 'market', time_in_force: str = 'day') -> Dict[str, Any]:
        """
        Place an order while enforcing risk controls.
        """
        if side.lower() not in ['buy', 'sell']:
            return {"error": "Side must be buy or sell."}
            
        if qty <= 0:
            return {"error": "Quantity must be greater than zero."}
            
        payload = {
            "symbol": symbol.upper(),
            "qty": str(qty),
            "side": side.lower(),
            "type": order_type.lower(),
            "time_in_force": time_in_force.lower()
        }
        
        logger.info(f"Placing {side} order for {qty} shares of {symbol}...")
        res = self._make_request('POST', 'v2/orders', data=payload)
        return res
