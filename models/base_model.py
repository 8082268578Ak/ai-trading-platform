import os
import joblib
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("models.base")

class BaseMLModel(ABC):
    """Abstract base class for all trading models."""
    
    def __init__(self, name: str):
        self.name = name
        self.model = None
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        
    @abstractmethod
    def prepare_data(self, df: pd.DataFrame, target_col: str):
        pass
        
    @abstractmethod
    def train(self, X_train, y_train, X_test, y_test):
        pass
        
    @abstractmethod
    def predict(self, X):
        pass
        
    def save(self):
        """Save standard scikit-learn models. Override for deep learning."""
        if self.model is None:
            logger.error(f"No model to save for {self.name}")
            return
            
        model_path = os.path.join(Config.MODEL_DIR, f"{self.name}.joblib")
        scaler_X_path = os.path.join(Config.MODEL_DIR, f"{self.name}_scaler_X.joblib")
        scaler_y_path = os.path.join(Config.MODEL_DIR, f"{self.name}_scaler_y.joblib")
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler_X, scaler_X_path)
        joblib.dump(self.scaler_y, scaler_y_path)
        logger.info(f"Saved {self.name} model and scalers.")
        
    def load(self):
        """Load standard scikit-learn models."""
        model_path = os.path.join(Config.MODEL_DIR, f"{self.name}.joblib")
        scaler_X_path = os.path.join(Config.MODEL_DIR, f"{self.name}_scaler_X.joblib")
        scaler_y_path = os.path.join(Config.MODEL_DIR, f"{self.name}_scaler_y.joblib")
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            self.scaler_X = joblib.load(scaler_X_path)
            self.scaler_y = joblib.load(scaler_y_path)
            logger.info(f"Loaded {self.name} model and scalers.")
            return True
        else:
            logger.warning(f"Model file not found for {self.name}")
            return False
