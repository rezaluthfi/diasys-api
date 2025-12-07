# Evaluate model and save metrics

import pickle
import pandas as pd
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split

# Load model and scaler
with open('models/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load dataset
df = pd.read_csv('diabetes.csv')

# Prepare features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split data (same ratio as training, typically 80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
X_test_scaled = scaler.transform(X_test)

# Predict
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# Prepare metrics
metrics = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "confusion_matrix": {
        "true_negative": int(cm[0][0]),
        "false_positive": int(cm[0][1]),
        "false_negative": int(cm[1][0]),
        "true_positive": int(cm[1][1])
    },
    "total_samples": len(y_test),
    "model_type": "Random Forest Classifier"
}

# Save to JSON
with open('models/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

print("Model Metrics:")
print(f"Accuracy: {metrics['accuracy']}%")
print(f"Precision: {metrics['precision']}%")
print(f"Recall: {metrics['recall']}%")
print(f"F1-Score: {metrics['f1_score']}%")
print(f"\nMetrics saved to models/model_metrics.json")
