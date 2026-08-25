import os
import joblib
import numpy as np

class MLEnsemble:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        xgb_path = os.path.join(models_dir, 'xgb_model.joblib')
        rf_path = os.path.join(models_dir, 'rf_model.joblib')
        
        self.xgb_model = None
        self.rf_model = None
        
        if os.path.exists(xgb_path):
            try:
                self.xgb_model = joblib.load(xgb_path)
            except Exception as e:
                print(f"[!] Failed to load XGB model: {e}")
                
        if os.path.exists(rf_path):
            try:
                self.rf_model = joblib.load(rf_path)
            except Exception as e:
                print(f"[!] Failed to load RF model: {e}")
            
    def predict(self, feature_vector: list[float]) -> dict:
        """
        Passes the feature vector through XGBoost and Random Forest ensemble.
        """
        if not self.xgb_model and not self.rf_model:
            return {
                "model": "fallback-rules",
                "version": "1.0.0",
                "prediction": "UNKNOWN",
                "confidence": 0.5,
                "model_breakdown": {
                    "xgboost": 0.5,
                    "random_forest": 0.5
                }
            }
            
        X_input = np.array([feature_vector])
        
        xgb_prob = 0.5
        rf_prob = 0.5
        
        if self.xgb_model:
            try:
                xgb_pred_proba = self.xgb_model.predict_proba(X_input)[0]
                xgb_prob = float(xgb_pred_proba[1])
            except Exception:
                pass
                
        if self.rf_model:
            try:
                rf_pred_proba = self.rf_model.predict_proba(X_input)[0]
                rf_prob = float(rf_pred_proba[1])
            except Exception:
                rf_prob = xgb_prob
        else:
            rf_prob = xgb_prob
            
        # Ensemble weighted probability
        ensemble_prob = float(0.55 * xgb_prob + 0.45 * rf_prob)
        classification = "PHISHING" if ensemble_prob >= 0.5 else "LEGITIMATE"
        
        return {
            "model": "ensemble (xgboost + random forest)",
            "version": "2.0.0",
            "prediction": classification,
            "confidence": ensemble_prob,
            "model_breakdown": {
                "xgboost": round(xgb_prob, 4),
                "random_forest": round(rf_prob, 4),
                "ensemble": round(ensemble_prob, 4)
            }
        }
