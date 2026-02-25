FROM python:3.11-slim

WORKDIR /app

COPY processed_heart.csv .
COPY heart_disease_model.pkl .
COPY api.py .

RUN pip install pandas scikit-learn joblib flask --no-cache-dir

CMD ["python", "api.py"]