# ===============================
# Imports
# ===============================
import os
import pandas as pd
from flask import Flask, request, jsonify
import joblib

# ===============================
# Create data folder automatically
# ===============================
os.makedirs("data", exist_ok=True)

# ===============================
# Initialize Flask App
# ===============================
app = Flask(__name__)

# ===============================
# Load Trained Model
# ===============================
model = joblib.load("heart_disease_model.pkl")


# ===============================
# Production Data Logger
# ===============================
def log_production_data(input_data):
    """
    Save incoming prediction requests
    for drift detection monitoring
    """

    df = pd.DataFrame([input_data])

    file_path = "data/production_data.csv"

    df.to_csv(
        file_path,
        mode="a",
        header=not os.path.exists(file_path),
        index=False
    )


# ===============================
# Home Route
# ===============================
@app.route('/')
def home():
    return jsonify({
        "message": "Heart Disease MLOps API Running"
    })


# ===============================
# Health Check
# ===============================
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy"
    })


# ===============================
# Prediction Endpoint
# ===============================
@app.route('/predict', methods=['POST'])
def predict():

    try:
        # Get input JSON
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400

        # Log original production data
        log_production_data(data)

        # Convert input to DataFrame
        df = pd.DataFrame([data])

        # Map API feature names to model feature names
        df = df.rename(columns={
            'cp': 'chest_pain_type',
            'trestbps': 'resting_blood_pressure',
            'chol': 'cholestoral',
            'fbs': 'fasting_blood_sugar',
            'restecg': 'rest_ecg',
            'thalach': 'Max_heart_rate',
            'exang': 'exercise_induced_angina',
            'ca': 'vessels_colored_by_flourosopy',
            'thal': 'thalassemia'
        })

        # Ensure correct feature order
        feature_columns = [
            'age',
            'sex',
            'chest_pain_type',
            'resting_blood_pressure',
            'cholestoral',
            'fasting_blood_sugar',
            'rest_ecg',
            'Max_heart_rate',
            'exercise_induced_angina',
            'oldpeak',
            'slope',
            'vessels_colored_by_flourosopy',
            'thalassemia'
        ]

        df = df[feature_columns]

        # Prediction
        prediction = model.predict(df)

        return jsonify({
            "Predicted target": int(prediction[0])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )