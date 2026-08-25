import numpy as np

class FeatureEngine:
    def extract_features(self, analysis_results: dict) -> list[float]:
        """
        Converts the raw nested dictionary from analyzers into the flat 
        numeric array expected by the ML models.
        """
        try:
            url_data = analysis_results.get("url", {})
            
            # Must strictly match the feature order in training!
            # The current trained model drops length bias. Features:
            # ['subdomain_count', 'has_ip', 'entropy', 'keyword_count']
            
            features = [
                float(url_data.get("subdomain_count", 0)),
                float(1 if url_data.get("has_ip", False) else 0),
                float(url_data.get("entropy", 0.0)),
                float(len(url_data.get("suspicious_keywords", [])))
            ]
            
            return features
            
        except Exception as e:
            print(f"[!] FeatureEngine extraction failed: {e}")
            return [0.0, 0.0, 0.0, 0.0] # Fallback vector
