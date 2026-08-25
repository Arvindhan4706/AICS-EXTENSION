import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class EmailNLPEnsemble:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.rf_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
        self.is_trained = False
        
        self.model_dir = os.path.dirname(os.path.abspath(__file__))
        self.vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
        self.model_path = os.path.join(self.model_dir, 'email_rf_model.pkl')
        
        self._load_or_train()

    def _load_or_train(self):
        if os.path.exists(self.vectorizer_path) and os.path.exists(self.model_path):
            try:
                with open(self.vectorizer_path, 'rb') as vf:
                    self.vectorizer = pickle.load(vf)
                with open(self.model_path, 'rb') as mf:
                    self.rf_model = pickle.load(mf)
                self.is_trained = True
                print("Loaded Email NLP model from disk.")
                return
            except Exception as e:
                print(f"Error loading model: {e}")
                
        self.train_on_dataset()
        
    def train_on_dataset(self):
        dataset_path = r'd:\Class 12\AICS REVIEW\archive (6)\Phishing_Email.csv'
        if not os.path.exists(dataset_path):
            print("Email dataset not found. Model will not be trained.")
            return
            
        print("Training Email NLP model... This may take a moment.")
        try:
            # We skip bad lines to avoid the unicode errors found during research
            df = pd.read_csv(dataset_path, engine='python', on_bad_lines='skip')
            df.dropna(subset=['Email Text', 'Email Type'], inplace=True)
            
            X_text = df['Email Text'].astype(str).tolist()
            y = df['Email Type'].apply(lambda x: 1 if 'Phishing' in str(x) else 0).tolist()
            
            # --- OMNI-DATASET NLP PIPELINE ---
            # Append archive (7) spam.csv
            spam_path = r'd:\Class 12\AICS REVIEW\archive (7)\spam.csv'
            if os.path.exists(spam_path):
                try:
                    df_spam = pd.read_csv(spam_path, engine='python', on_bad_lines='skip')
                    if 'v2' in df_spam.columns and 'v1' in df_spam.columns:
                        X_spam = df_spam['v2'].astype(str).tolist()
                        y_spam = df_spam['v1'].apply(lambda x: 1 if 'spam' in str(x).lower() else 0).tolist()
                        X_text.extend(X_spam)
                        y.extend(y_spam)
                        print(f"OMNI-MERGE: Appended {len(X_spam)} rows from spam.csv")
                except Exception as e:
                    pass

            # Append archive (10) and (11) phishing_email_detection_2026_dataset.csv
            for arch_num in ['10', '11']:
                p_path = rf'd:\Class 12\AICS REVIEW\archive ({arch_num})\phishing_email_detection_2026_dataset.csv'
                if os.path.exists(p_path):
                    try:
                        df_p = pd.read_csv(p_path, engine='python', on_bad_lines='skip')
                        if 'subject' in df_p.columns and 'is_phishing' in df_p.columns:
                            # Use subject as text approximation
                            X_p = df_p['subject'].astype(str).tolist()
                            y_p = df_p['is_phishing'].apply(lambda x: 1 if str(x) == '1' else 0).tolist()
                            X_text.extend(X_p)
                            y.extend(y_p)
                            print(f"OMNI-MERGE: Appended {len(X_p)} rows from archive ({arch_num}) 2026 dataset")
                    except Exception as e:
                        pass
            
            # Subsample for speed if massive
            if len(X_text) > 15000:
                import random
                combined = list(zip(X_text, y))
                random.shuffle(combined)
                combined = combined[:15000]
                X_text, y = zip(*combined)
                X_text = list(X_text)
                y = list(y)
                
            X_vec = self.vectorizer.fit_transform(X_text)
            self.rf_model.fit(X_vec, y)
            
            with open(self.vectorizer_path, 'wb') as vf:
                pickle.dump(self.vectorizer, vf)
            with open(self.model_path, 'wb') as mf:
                pickle.dump(self.rf_model, mf)
                
            self.is_trained = True
            print("Email NLP model trained and saved to disk.")
        except Exception as e:
            print(f"Failed to train email NLP model: {e}")

    def predict(self, email_text: str) -> dict:
        if not self.is_trained or not email_text.strip():
            return {'threat_score': 0, 'probability': 0.0}
            
        X_vec = self.vectorizer.transform([email_text])
        prob = float(self.rf_model.predict_proba(X_vec)[0][1])
        
        return {
            'threat_score': int(prob * 100),
            'probability': prob
        }

# Global instance for the router to import
email_nlp_engine = EmailNLPEnsemble()
