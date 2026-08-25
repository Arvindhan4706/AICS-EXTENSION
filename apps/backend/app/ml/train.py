import pandas as pd
import numpy as np
import urllib.parse
import math
import re
import joblib
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import os

# Define Suspicious Keywords (same as URLAnalyzer)
SUSPICIOUS_KEYWORDS = ["verify", "account", "login", "secure", "bank", "update", "paypal"]

def calculate_entropy(string: str) -> float:
    if not string:
        return 0.0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

def extract_features(df):
    print("Extracting features (this may take a minute for 500k+ rows)...")
    
    # Fast extraction using Pandas apply and vectorization
    
    # 1. URL Length
    df['url_length'] = df['URL'].str.len()
    
    # 2. Hostname parsing
    def get_hostname(url):
        try:
            if not str(url).startswith('http'):
                url = 'http://' + str(url)
            return urllib.parse.urlparse(url).hostname or ""
        except ValueError:
            return ""
        
    print("Parsing hostnames...")
    df['hostname'] = df['URL'].apply(get_hostname)
    df['hostname_length'] = df['hostname'].str.len()
    
    # 3. Subdomain count
    df['subdomain_count'] = df['hostname'].apply(lambda x: x.count('.') - 1 if x.count('.') > 0 else 0)
    
    # 4. Has IP
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    df['has_ip'] = df['hostname'].apply(lambda x: 1 if ip_pattern.match(x) else 0)
    
    # 5. Entropy
    print("Calculating entropy...")
    df['entropy'] = df['hostname'].apply(calculate_entropy)
    
    # 6. Suspicious Keyword Count
    print("Counting suspicious keywords...")
    def count_keywords(url):
        url_lower = url.lower()
        return sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)
        
    df['keyword_count'] = df['URL'].apply(count_keywords)
    
    # Label encoding: bad=1, good=0
    df['label_binary'] = df['Label'].map({'bad': 1, 'good': 0})
    
    features = ['subdomain_count', 'has_ip', 'entropy', 'keyword_count']
    return df[features], df['label_binary']

def train_models():
    dataset_path = r"d:\Class 12\AICS-EXTENSION\phishing_site_urls.csv"
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return
        
    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df)} rows.")
    
    start_time = time.time()
    X, y = extract_features(df)
    
    # Handle any potential NaNs (though shouldn't happen with our extraction)
    X = X.fillna(0)
    y = y.fillna(0)
    print(f"Feature extraction completed in {time.time() - start_time:.2f} seconds.")
    
    print("Splitting dataset (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("\nTraining Random Forest...")
    rf_start = time.time()
    rf = RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    print(f"Random Forest trained in {time.time() - rf_start:.2f} seconds.")
    print("Random Forest Accuracy:", accuracy_score(y_test, rf_pred))
    
    # Train XGBoost
    print("\nTraining XGBoost...")
    xgb_start = time.time()
    xgb = XGBClassifier(n_estimators=100, max_depth=10, learning_rate=0.1, n_jobs=-1, random_state=42)
    xgb.fit(X_train, y_train)
    xgb_pred = xgb.predict(X_test)
    print(f"XGBoost trained in {time.time() - xgb_start:.2f} seconds.")
    print("XGBoost Accuracy:", accuracy_score(y_test, xgb_pred))
    
    # Detailed Report for XGBoost (Primary Model)
    print("\nXGBoost Classification Report:")
    print(classification_report(y_test, xgb_pred, target_names=["Legitimate (0)", "Phishing (1)"]))
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save models
    rf_path = os.path.join(models_dir, 'rf_model.joblib')
    xgb_path = os.path.join(models_dir, 'xgb_model.joblib')
    
    print(f"\nSaving models to {models_dir}...")
    joblib.dump(rf, rf_path)
    joblib.dump(xgb, xgb_path)
    
    print("Training pipeline complete!")

if __name__ == "__main__":
    train_models()
