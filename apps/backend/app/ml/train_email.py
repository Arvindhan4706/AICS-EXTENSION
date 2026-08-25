import os
import pandas as pd
import joblib
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_email_model():
    print("[*] Initializing Email NLP Training Pipeline...")
    start_time = time.time()
    
    csv_path = r"d:\Class 12\AICS-EXTENSION\Phishing_Email.csv"
    if not os.path.exists(csv_path):
        print(f"[!] Dataset not found at {csv_path}")
        return
        
    print(f"[*] Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path).dropna()
    
    # Standardize column names
    text_col = 'Email Text'
    label_col = 'Email Type'
    
    # Limit dataset size for performance during local dev (e.g. 30k samples)
    if len(df) > 30000:
        df = df.sample(30000, random_state=42)
    
    # Map labels: Safe Email -> 0, Phishing Email -> 1
    df['label'] = df[label_col].map(lambda x: 1 if 'Phishing' in str(x) else 0)
    
    X = df[text_col].astype(str)
    y = df['label']
    
    print(f"[*] Extracting TF-IDF Features (max 1000 features)...")
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X_tfidf = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
    
    print("[*] Training Random Forest NLP Model (n_estimators=30)...")
    model = RandomForestClassifier(n_estimators=30, max_depth=20, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[*] Training Complete! Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, y_pred))
    
    # Ensure models dir exists
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save artifacts
    vectorizer_path = os.path.join(models_dir, 'email_vectorizer.joblib')
    model_path = os.path.join(models_dir, 'email_model.joblib')
    
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    
    print(f"[*] Artifacts saved to {models_dir}")
    print(f"[*] Time taken: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    train_email_model()
