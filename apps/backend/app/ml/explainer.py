import os
import joblib

class SHAPExplainer:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        xgb_path = os.path.join(models_dir, 'xgb_model.joblib')
        
        self.xgb_model = None
        self.feature_names = ['subdomain_count', 'has_ip', 'entropy', 'keyword_count']
        
        if os.path.exists(xgb_path):
            self.xgb_model = joblib.load(xgb_path)
            
    def explain(self, feature_vector: list[float], prediction: dict) -> list[dict]:
        """
        Generates human-readable explanations based on feature importance.
        """
        explanations = []
        
        if not self.xgb_model:
            explanations.append({
                "feature": "baseline",
                "importance": 0.05,
                "description": "No trained model found. Running on basic heuristics."
            })
            return explanations
            
        importances = self.xgb_model.feature_importances_
        
        # Match features with importances
        feature_impacts = list(zip(self.feature_names, feature_vector, importances))
        
        # Sort by importance
        feature_impacts.sort(key=lambda x: x[2], reverse=True)
        
        # Translate the top 3 driving features into human readable text
        for name, value, importance in feature_impacts[:3]:
            if importance > 0.05:
                desc = f"{name.replace('_', ' ').title()} was measured as {value:.2f}"
                if name == 'keyword_count' and value > 0:
                    desc = "Suspicious keywords detected in URL"
                elif name == 'has_ip' and value == 1:
                    desc = "IP Address used directly in URL"
                elif name == 'entropy' and value > 4.5:
                    desc = "High entropy (random character sequence) detected"
                elif name == 'url_length' and value > 75:
                    desc = "Unusually long URL length"
                elif name == 'subdomain_count' and value > 2:
                    desc = "Multiple subdomains detected"
                    
                explanations.append({
                    "feature": name,
                    "importance": round(float(importance), 2),
                    "description": f"{desc} (+{importance:.2f})"
                })
                
        if not explanations:
            explanations.append({
                "feature": "baseline",
                "importance": 0.05,
                "description": "No major single risk indicator dominated the decision."
            })
            
        return explanations
