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
    return jsonify({"message": "Heart Disease MLOps API Running"})


# ===============================
# Health Check (Kubernetes Uses This)
# ===============================
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


# ===============================
# Prediction Endpoint
# ===============================
@app.route('/predict', methods=['POST'])
def predict():

    try:
        # get input JSON
        data = request.get_json()

        # ⭐ log production data
        log_production_data(data)

        # convert to dataframe
        df = pd.DataFrame([data])

        # prediction
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
    app.run(host="0.0.0.0", port=5000)