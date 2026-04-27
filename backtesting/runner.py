import backtrader as bt
import pandas as pd
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("backtesting.runner")

class SignalData(bt.feeds.PandasData):
    """Custom Data Feed that includes 'Signal' column."""
    lines = ('signal',)
    params = (
        ('signal', -1), # Index of the column in pandas
    )

class AISignalStrategy(bt.Strategy):
    """Executes trades based on AI generated signals."""
    
    params = (
        ('stop_loss', Config.STOP_LOSS),
        ('take_profit', Config.TAKE_PROFIT),
    )
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logger.info(f"{dt.isoformat()} - {txt}")
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.signal = self.datas[0].signal
        self.order = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
            
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}")
            else:
                self.log(f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}")
            self.bar_executed = len(self)
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f"Order Canceled/Margin/Rejected. Status: {order.status}")
            
        self.order = None
        
    def next(self):
        if self.order:
            return # Pending order processing
            
        # Simplistic Risk Management / Position Sizing
        # Trade with 10% of portfolio value per signal
        portfolio_value = self.broker.getvalue()
        trade_size = (portfolio_value * 0.1) / self.dataclose[0]
        
        if not self.position:
            if self.signal[0] == 1:
                self.log(f"BUY SIGNAL generated. Price: {self.dataclose[0]:.2f}")
                self.order = self.buy(size=trade_size)
                
        else:
            # If we hold a position, look for sell signal or stoploss/takeprofit
            # For simplicity, exit on sell signal
            if self.signal[0] == -1:
                self.log(f"SELL SIGNAL generated. Closing position. Price: {self.dataclose[0]:.2f}")
                self.order = self.close()
                

class BacktestRunner:
    @staticmethod
    def run(df: pd.DataFrame, plot: bool = False):
        logger.info("Initializing Backtrader cerebro engine...")
        cerebro = bt.Cerebro()
        
        # Add strategy
        cerebro.addstrategy(AISignalStrategy)
        
        # Prepare data
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            
        # We need Open, High, Low, Close, Volume, and Signal
        req_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Signal']
        for col in req_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column for backtesting: {col}")
                
        data_df = df[req_cols].copy()
        data = SignalData(dataname=data_df)
        
        cerebro.adddata(data)
        cerebro.broker.setcash(Config.INITIAL_CASH)
        cerebro.broker.setcommission(commission=0.001) # 0.1% commission
        
        # Analyzers
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        
        logger.info(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
        results = cerebro.run()
        final_value = cerebro.broker.getvalue()
        logger.info(f"Final Portfolio Value: {final_value:.2f}")
        
        strat = results[0]
        metrics = {
            "final_value": final_value,
            "total_return": strat.analyzers.returns.get_analysis().get('rtot', 0),
            "sharpe_ratio": strat.analyzers.sharpe.get_analysis().get('sharperatio', 0),
            "max_drawdown": strat.analyzers.drawdown.get_analysis().get('max', {}).get('drawdown', 0)
        }
        
        logger.info(f"Backtest Metrics: {metrics}")
        
        if plot:
            cerebro.plot(style='candlestick')
            
        return metrics
