# ML Model loader

import pickle
import numpy as np
import json
from pathlib import Path

class DiabetesModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.metrics = None
        self._load_models()
        self._load_metrics()
    
    def _load_models(self):
        try:
            model_path = Path("models/diabetes_model.pkl")
            scaler_path = Path("models/scaler.pkl")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            print(f"✅ ML Model loaded")
        except Exception as e:
            print(f"⚠️ Warning: Could not load ML model - {e}")
    
    def _load_metrics(self):
        try:
            metrics_path = Path("models/model_metrics.json")
            with open(metrics_path, 'r') as f:
                self.metrics = json.load(f)
            print(f"✅ Model metrics loaded")
        except Exception as e:
            print(f"⚠️ Warning: Could not load metrics - {e}")
            self.metrics = None
    
    def predict(self, features):
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded")
        
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        return prediction, probability
    
    def get_metrics(self):
        return self.metrics
    
    @property
    def is_loaded(self):
        return self.model is not None and self.scaler is not None

# Global instance
diabetes_model = DiabetesModel()
