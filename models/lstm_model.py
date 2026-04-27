import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from models.base_model import BaseMLModel
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("models.lstm")

class LSTMPricePredictor(BaseMLModel):
    """LSTM model for time-series forecasting of stock prices."""
    
    def __init__(self, name="lstm_model"):
        super().__init__(name)
        self.seq_length = Config.SEQ_LENGTH
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = 'Close'):
        """
        Prepare sequence data for LSTM.
        Expects a dataframe with numerical features.
        """
        logger.info("Preparing data for LSTM...")
        # Fill/drop NaNs just in case
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        
        # We will use all columns as features, but scale target separately
        # to allow for easy inverse transformation later
        target_idx = df.columns.get_loc(target_col)
        
        data = df.values
        # Fit scalers
        self.scaler_X.fit(data)
        self.scaler_y.fit(data[:, target_idx].reshape(-1, 1))
        
        scaled_data = self.scaler_X.transform(data)
        
        X, y = [], []
        for i in range(self.seq_length, len(scaled_data)):
            X.append(scaled_data[i-self.seq_length:i, :])
            y.append(scaled_data[i, target_idx])
            
        X, y = np.array(X), np.array(y)
        
        # Split train/test
        split = int((1 - Config.TEST_SIZE) * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        logger.info(f"Data shapes: X_train={X_train.shape}, y_train={y_train.shape}")
        return X_train, X_test, y_train, y_test
        
    def build_model(self, input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=25))
        model.add(Dense(units=1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model
        
    def train(self, X_train, y_train, X_test, y_test):
        if self.model is None:
            self.build_model((X_train.shape[1], X_train.shape[2]))
            
        logger.info("Starting LSTM training...")
        history = self.model.fit(
            X_train, y_train,
            batch_size=Config.BATCH_SIZE,
            epochs=Config.EPOCHS,
            validation_data=(X_test, y_test),
            verbose=1
        )
        logger.info("LSTM training completed.")
        return history
        
    def predict(self, X):
        if self.model is None:
            raise ValueError("Model not trained or loaded.")
        pred = self.model.predict(X)
        return self.scaler_y.inverse_transform(pred)
        
    def save(self):
        super().save() # Saves scalers
        if self.model is not None:
            model_path = os.path.join(Config.MODEL_DIR, f"{self.name}.keras")
            self.model.save(model_path)
            logger.info(f"Saved LSTM model to {model_path}")
            
    def load(self):
        scaler_loaded = super().load()
        model_path = os.path.join(Config.MODEL_DIR, f"{self.name}.keras")
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            logger.info("Loaded LSTM model.")
            return True
        return False
