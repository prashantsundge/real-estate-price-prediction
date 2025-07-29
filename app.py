# app.py

import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model and preprocessing tools
model = joblib.load("artifacts/model/model.pkl")
scaler = joblib.load("artifacts/scaler/minmax_scaler.pkl")
transaction_encoder = joblib.load("artifacts/encoders/transaction_encoder.pkl")
furnishing_encoder = joblib.load("artifacts/encoders/furnishing_encoder.pkl")
possession_encoder = joblib.load("artifacts/encoders/possession_status_encoder.pkl")

# Title
st.title("🏠 Real Estate Price Predictor")

# Input fields
transaction = st.selectbox("Transaction", transaction_encoder.classes_)
furnishing = st.selectbox("Furnishing", furnishing_encoder.classes_)
possession_status = st.selectbox("Possession Status", possession_encoder.classes_)
bhk = st.number_input("BHK", min_value=1, max_value=10, value=3)
bathroom = st.number_input("Bathroom", min_value=0, max_value=10, value=2)
covered_parking = st.number_input("Covered Parking", min_value=0, max_value=3, value=1)
open_parking = st.number_input("Open Parking", min_value=0, max_value=3, value=0)
total_area = st.number_input("Total Area (sqft)", min_value=100, max_value=10000, value=1000)
price_per_sqft = st.number_input("Price per sqft", min_value=1000, max_value=20000, value=5000)

if st.button("Predict Price"):

    # Encode categorical variables
    transaction_encoded = transaction_encoder.transform([transaction])[0]
    furnishing_encoded = furnishing_encoder.transform([furnishing])[0]
    possession_encoded = possession_encoder.transform([possession_status])[0]

    # Create input DataFrame
    input_data = pd.DataFrame([{
        "Transaction": transaction_encoded,
        "Furnishing": furnishing_encoded,
        "Bathroom": bathroom,
        "Price per Sqft": price_per_sqft,
        "Total Area": total_area,
        "Covered_parking": covered_parking,
        "Open_parking": open_parking,
        "Possession_Status": possession_encoded,
        "BHK": bhk
    }])

    # Apply scaling without feature names to avoid mismatch
    scaled_values = scaler.transform(input_data[["Total Area", "Price per Sqft"]].values)
    input_data["Total Area"] = scaled_values[:, 0]
    input_data["Price per Sqft"] = scaled_values[:, 1]


    # Make prediction
    prediction = model.predict(input_data)[0]

    # Show prediction
    st.success(f"🏷️ Predicted Price: ₹ {prediction:,.0f}")
