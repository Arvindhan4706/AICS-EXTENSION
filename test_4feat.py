import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import urllib.parse
import re
import math
import numpy as np

dataset_path = r"d:\Class 12\AICS-EXTENSION\phishing_site_urls.csv"
print("Reading dataset...")
df = pd.read_csv(dataset_path)

def get_hostname(url):
    try:
        if not str(url).startswith('http'):
            url = 'http://' + str(url)
        return urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        return ""

def calculate_entropy(string: str) -> float:
    if not string:
        return 0.0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

print("Extracting features...")
df['hostname'] = df['URL'].apply(get_hostname)
df['subdomain_count'] = df['hostname'].apply(lambda x: x.count('.') - 1 if x.count('.') > 0 else 0)
ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
df['has_ip'] = df['hostname'].apply(lambda x: 1 if ip_pattern.match(x) else 0)
df['entropy'] = df['hostname'].apply(calculate_entropy)

SUSPICIOUS_KEYWORDS = ["verify", "account", "login", "secure", "bank", "update", "paypal"]
def count_keywords(url):
    url_lower = url.lower()
    return sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)
df['keyword_count'] = df['URL'].apply(count_keywords)

df['label_binary'] = df['Label'].map({'bad': 1, 'good': 0})
features = ['subdomain_count', 'has_ip', 'entropy', 'keyword_count']
X = df[features].fillna(0)
y = df['label_binary'].fillna(0)

print("Training XGBoost...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xgb = XGBClassifier(n_estimators=100, max_depth=10, learning_rate=0.1, n_jobs=-1, random_state=42)
xgb.fit(X_train, y_train)
preds = xgb.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

X_new = pd.DataFrame([[0.0, 0.0, 3.32, 0.0]], columns=features)
print("Google:", xgb.predict_proba(X_new))
