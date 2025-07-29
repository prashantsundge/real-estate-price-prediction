import joblib
import numpy as np
from src.models.schemas import PropertyFeatures

# Load model and transformers
model = joblib.load("artifacts/model.pkl")
transaction_encoder = joblib.load("artifacts/encoders/transaction_encoder.pkl")
furnishing_encoder = joblib.load("artifacts/encoders/furnishing_encoder.pkl")
possession_encoder = joblib.load("artifacts/encoders/possession_status_encoder.pkl")
scaler = joblib.load("artifacts/scaler/minmax_scaler.pkl")

def predict_price(data: PropertyFeatures) -> float:
    encoded = [
        transaction_encoder.transform([data.Transaction])[0],
        furnishing_encoder.transform([data.Furnishing])[0],
        data.Bathroom,
        data.Price_per_Sqft,
        data.Total_Area,
        data.Covered_parking,
        data.Open_parking,
        possession_encoder.transform([data.Possession_Status])[0],
        data.BHK,
    ]

    # Normalize continuous columns (index 3 and 4)
    norm_vals = scaler.transform([encoded[3:5]])[0]
    encoded[3] = norm_vals[0]
    encoded[4] = norm_vals[1]

    prediction = model.predict([encoded])[0]
    return round(prediction, 2)
