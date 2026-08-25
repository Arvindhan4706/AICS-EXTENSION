import os
import joblib

class MLEmailClassifier:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        vectorizer_path = os.path.join(models_dir, 'email_vectorizer.joblib')
        model_path = os.path.join(models_dir, 'email_model.joblib')
        
        try:
            self.vectorizer = joblib.load(vectorizer_path)
            self.model = joblib.load(model_path)
            self.ready = True
        except Exception as e:
            print(f"[!] Warning: Email ML models not found or failed to load. Run train_email.py first. ({e})")
            self.ready = False

    def predict(self, email_text: str):
        if not self.ready:
            # Fallback mock if models are missing
            return {
                "threat_score": 15,
                "risk_level": "LOW",
                "explanations": [{"feature": "System Status", "importance": 1.0, "description": "NLP Engine offline. Defaulting to safe."}]
            }
            
        # 1. Vectorize text
        X_tfidf = self.vectorizer.transform([email_text])
        
        # 2. Predict probability
        prob = self.model.predict_proba(X_tfidf)[0][1] # Probability of class 1 (Phishing)
        threat_score = int(prob * 100)
        
        # 3. Basic feature extraction (Approximation of SHAP for performance)
        # We find which words in this email had the highest TF-IDF weight and combine them with the RandomForest feature importances
        feature_names = self.vectorizer.get_feature_names_out()
        importances = self.model.feature_importances_
        
        # Get non-zero features in this specific email
        nonzero_indices = X_tfidf.nonzero()[1]
        
        # Calculate a combined score for each word: (TF-IDF weight) * (RF Importance)
        word_scores = []
        for idx in nonzero_indices:
            word = feature_names[idx]
            weight = X_tfidf[0, idx]
            importance = importances[idx]
            word_scores.append((word, weight * importance, weight, importance))
            
        # Sort by highest combined impact
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        explanations = []
        for word, impact, weight, importance in word_scores[:5]:
            if impact > 0:
                explanations.append({
                    "feature": f"Keyword: '{word}'",
                    "importance": round(float(importance), 4),
                    "description": f"The presence and frequency of the word '{word}' strongly influenced the model's phishing classification."
                })
                
        if len(explanations) == 0:
             explanations.append({
                 "feature": "Text Structure",
                 "importance": 0.1,
                 "description": "No specific high-risk keywords dominated the classification."
             })
             
        risk_level = "CRITICAL" if threat_score > 70 else ("HIGH" if threat_score > 40 else ("MEDIUM" if threat_score > 20 else "LOW"))

        return {
            "threat_score": threat_score,
            "risk_level": risk_level,
            "explanations": explanations
        }
