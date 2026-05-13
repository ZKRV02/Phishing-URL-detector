import pandas as pd 
import glob
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


df = glob.glob('maybefinallysomeimprovement/archive/urls_*.csv')

df_list = [pd.read_csv(f) for f in df]

df_combined = pd.concat(df_list, ignore_index=True)

model = RandomForestClassifier()
features = [
    'dots', 'at', 'equals', 'slashes', 'hyphens', 'digits', 
    'is_https', 'url_length', 'is_domain_ip', 'subdomains', 
    'special_chars', 'digit_to_length_ratio'
]

X = df_combined[features]
y = df_combined['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100,n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
