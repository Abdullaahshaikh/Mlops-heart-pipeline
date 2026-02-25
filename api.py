from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load("heart_disease_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get JSON data
    df = pd.DataFrame([data])  # Convert to DataFrame
    prediction = model.predict(df)
    return jsonify({"Predicted target": int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)