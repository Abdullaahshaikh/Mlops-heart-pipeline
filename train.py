
import pandas as pd
import os
import json
import joblib

from codecarbon import EmissionsTracker
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ===============================
# 1. Load Dataset
# ===============================
df = pd.read_csv("processed_heart.csv")

X = df.drop("target", axis=1)
y = df["target"]

# ===============================
# 2. Train Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===============================
# 3. Model Training + Carbon Measurement
# ===============================
tracker = EmissionsTracker(
    project_name="heart_disease_training",
    output_file="carbon_emissions.csv"
)

tracker.start()

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

emissions = tracker.stop()

print(f"CO2 emissions: {emissions:.8f} kg")

# ===============================
# 4. Evaluation
# ===============================
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {acc*100:.2f}%\n")

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ===============================
# 5. Save Model
# ===============================
joblib.dump(model, "heart_disease_model.pkl")
print("\nModel saved as heart_disease_model.pkl")

# ===============================
# 6. Save Baseline Metrics
# ===============================
report_dict = classification_report(y_test, y_pred, output_dict=True)

baseline_metrics = {
    "accuracy": [acc],
    "precision_0": [report_dict['0']['precision']],
    "recall_0": [report_dict['0']['recall']],
    "f1_0": [report_dict['0']['f1-score']],
    "precision_1": [report_dict['1']['precision']],
    "recall_1": [report_dict['1']['recall']],
    "f1_1": [report_dict['1']['f1-score']]
}

pd.DataFrame(baseline_metrics).to_csv(
    "baseline_model_performance.csv",
    index=False
)

print("Baseline performance saved!")

# ===============================
# 7. SAVE DRIFT REFERENCE (PAPER PART)
# ===============================
os.makedirs("model", exist_ok=True)
os.makedirs("data", exist_ok=True)

train_stats = {}

for col in X_train.columns:
    train_stats[col] = {
        "mean": float(X_train[col].mean()),
        "std": float(X_train[col].std())
    }

with open("model/training_stats.json", "w") as f:
    json.dump(train_stats, f)

X_train.to_csv("data/train_reference.csv", index=False)

print("Training stats & reference data saved!")

