import os
import joblib

class MLEnsemble:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        xgb_path = os.path.join(models_dir, 'xgb_model.joblib')
        
        self.xgb_model = None
        if os.path.exists(xgb_path):
            self.xgb_model = joblib.load(xgb_path)
            
    def predict(self, feature_vector: list[float]) -> dict:
        """
        Passes the feature vector through the XGBoost model.
        """
        if not self.xgb_model:
            # Fallback if model not trained
            return {
                "model": "fallback-rules",
                "version": "1.0.0",
                "prediction": "UNKNOWN",
                "confidence": 0.5
            }
            
        # The model expects a 2D array: shape (1, n_features)
        import numpy as np
        X_input = np.array([feature_vector])
        
        # XGBoost output
        pred_class = self.xgb_model.predict(X_input)[0]
        pred_proba = self.xgb_model.predict_proba(X_input)[0]
        
        confidence = float(pred_proba[1]) # Probability of being phishing (class 1)
        
        classification = "PHISHING" if pred_class == 1 else "LEGITIMATE"
        
        return {
            "model": "xgboost",
            "version": "1.0.0",
            "prediction": classification,
            "confidence": confidence
        }
