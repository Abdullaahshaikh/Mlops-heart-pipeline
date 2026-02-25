import pandas as pd
import joblib


# Load model
model = joblib.load("heart_disease_model.pkl")

# Load first row of data for prediction
data = pd.read_csv("processed_heart.csv")
sample = data.iloc[0:1, :-1]  # remove target column

# Predict
prediction = model.predict(sample)
print("Predicted target:", prediction[0])