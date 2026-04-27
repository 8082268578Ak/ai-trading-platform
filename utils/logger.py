import logging
import os
import sys
from config.settings import Config

def get_logger(name: str) -> logging.Logger:
    """
    Setup and return a structured logger.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Optional: File handler
        log_dir = os.path.join(Config.BASE_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
