import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from models.base_model import BaseMLModel
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("models.xgb")

class XGBoostPredictor(BaseMLModel):
    """XGBoost Regressor for predicting next day returns."""
    
    def __init__(self, name="xgb_model"):
        super().__init__(name)
        self.model = xgb.XGBRegressor(
            n_estimators=100, 
            learning_rate=0.05, 
            max_depth=5, 
            random_state=42
        )
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = 'Target_Return'):
        """
        Prepare tabular data for XGBoost.
        """
        logger.info("Preparing data for XGBoost...")
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        
        X = df.drop(columns=[target_col, 'Target_Class', 'Next_Close'], errors='ignore')
        y = df[target_col]
        
        split = int((1 - Config.TEST_SIZE) * len(X))
        
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]
        
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        X_test_scaled = self.scaler_X.transform(X_test)
        
        y_train_scaled = self.scaler_y.fit_transform(y_train.values.reshape(-1, 1)).ravel()
        y_test_scaled = self.scaler_y.transform(y_test.values.reshape(-1, 1)).ravel()
        
        logger.info(f"Data shapes: X_train={X_train_scaled.shape}")
        return X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled
        
    def train(self, X_train, y_train, X_test, y_test):
        logger.info("Training XGBoost model...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        preds = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        
        logger.info(f"XGB Training complete. RMSE: {rmse:.4f}, MAE: {mae:.4f}")
        return {"rmse": rmse, "mae": mae}
        
    def predict(self, X):
        if self.model is None:
            raise ValueError("Model not trained.")
        preds = self.model.predict(X)
        return self.scaler_y.inverse_transform(preds.reshape(-1, 1)).ravel()
