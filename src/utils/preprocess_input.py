
import numpy as np 
import pandas as pd

import joblib
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

#load the encoders and scaler 

label_encoders = {

    "Transaction": joblib.load("artificats/encoders/transaction_encoder.pkl"),
    "Furnishing": joblib.load("artificats/encoders/furnishing_encoder.pkl"),
    "Possession_Status": joblib.load("artifacts/encoders/possession_status_encoder.pkl"),
    
}

scaler = joblib.load("artifacts/scaler/minmax_scaler.pkl")

def preprocess_input (user_input:dict) ->np.ndarray:
    """"
    Process raw streamlit input dict into model -ready numpy array
        """
    
    df = pd.DataFrame([user_input])
       # Label encode categorical columns
    for col in ["Transaction", "Furnishing", "Possession_Status"]:
        le = label_encoders[col]
        df[col] = le.transform(df[col].astype(str))

    # Drop unused or high-cardinality columns if present
    df = df.drop(columns=["Society", "Possession"], errors="ignore")

    # Scale continuous features
    for col in ["Price per Sqft", "Total Area"]:
        if col in df.columns:
            df[col] = scaler.transform(df[[col]])

    return df.values