import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

dataset_path = r"d:\Class 12\AICS-EXTENSION\phishing_site_urls.csv"
print("Loading data...")
df = pd.read_csv(dataset_path)

# Drop corrupted rows (where URL or Label is null)
df = df.dropna()

print(f"Data shape: {df.shape}")
df['label_binary'] = df['Label'].map({'bad': 1, 'good': 0})
df = df.dropna(subset=['label_binary'])

print("Vectorizing...")
t0 = time.time()
vectorizer = TfidfVectorizer(max_features=5000, analyzer='char', ngram_range=(3, 5))
X = vectorizer.fit_transform(df['URL'])
y = df['label_binary']
print(f"Vectorized in {time.time()-t0:.2f}s")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training LR...")
t0 = time.time()
lr = LogisticRegression(max_iter=1000, n_jobs=-1)
lr.fit(X_train, y_train)
print(f"LR trained in {time.time()-t0:.2f}s")

preds = lr.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

test_urls = ["google.com", "example.com", "paypal.com-verify-account.update.xyz", "http://192.168.1.1/login"]
X_new = vectorizer.transform(test_urls)
print("Test predictions:", lr.predict_proba(X_new))
