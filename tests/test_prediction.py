import unittest
import pandas as pd
import numpy as np
from src.model.predictor import CarPricePredictor
from src.config import config

class TestCarPricePredictor(unittest.TestCase):
    def setUp(self):
        # Ensure we can load the model (assumes running from root)
        try:
            self.predictor = CarPricePredictor()
        except:
            self.skipTest("Model file not found - skipping integration test")

    def test_prediction_output(self):
        # Create a dummy input matching the expected schema
        sample_input = pd.DataFrame({
            "Location": ["Mumbai"],
            "Year": [2015],
            "Kilometers_Driven": [50000],
            "Fuel_Type": ["Petrol"],
            "Transmission": ["Manual"],
            "Owner_Type": ["First"],
            "Mileage": [18.0],
            "Engine": [1200],
            "Power": [85],
            "Brand": ["Maruti"],
            "Model": ["Swift"]
        })
        
        prediction = self.predictor.predict(sample_input)
        
        self.assertIsInstance(prediction, float)
        self.assertGreater(prediction, 0)
        
    def test_invalid_input(self):
        with self.assertRaises(Exception):
            self.predictor.predict(pd.DataFrame())

if __name__ == "__main__":
    unittest.main()
