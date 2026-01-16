import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Union
from src.config import config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

class CarPricePredictor:
    def __init__(self):
        self.model_path = config.get("paths.model")
        self.model = self._load_model()

    def _load_model(self):
        """Load the trained machine learning model."""
        try:
            logger.info(f"Loading model from {self.model_path}")
            with open(self.model_path, "rb") as f:
                model = pickle.load(f)
            logger.info("Model loaded successfully")
            return model
        except FileNotFoundError:
            logger.error(f"Model file not found at {self.model_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, features: pd.DataFrame) -> float:
        """
        Make a prediction based on input features.
        
        Args:
            features (pd.DataFrame): DataFrame containing valid feature columns.
            
        Returns:
            float: The predicted price (transformed back to original scale).
        """
        try:
            # Basic validation
            if features.empty:
                raise ValueError("Features DataFrame is empty")

            logger.info("Running prediction")
            raw_prediction = self.model.predict(features)
            
            # Post-processing as per original code logic
            # prediction = np.expm1(prediction) * 1200
            price = np.expm1(raw_prediction[0]) * config.get("model.prediction_multiplier", 1200)
            
            logger.info(f"Prediction successful: {price}")
            return max(0.0, price) # Ensure no negative prices
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
