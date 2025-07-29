
#src/model/train_model.py

import os 
import pandas as pd 
import joblib
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error , mean_absolute_error , r2_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from src.utils.logger import logger


def train_model(data_path: str ="notebooks\data\processed\clean_df.csv", model_path:str = "artifacts/model.pkl" ):
    logger.info("Loading Data for Training...")
    df = pd.read_csv(data_path)

    x = df[["Transaction",	"Furnishing",	"Bathroom",	"Price per Sqft"	,"Total Area"	, "Covered_parking"	,"Open_parking",	"Possession_Status",	"BHK"]]

    y = df["Price_INR_Numeric"]

    X_train, X_test, y_train , y_test = train_test_split(x,y,test_size=0.2, random_state=42)

    logger.info("Training Linear Regression Model...")
    model  = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test , y_pred)
    mae = mean_absolute_error(y_test , y_pred)
    r2 = r2_score(y_test , y_pred)

    logger.info(f"Model RMSE : {rmse :.2f}")
    logger.info(f"Model Mean absolute error : {mae :.2f}")
    logger.info(f"Model R2 Score : {r2 :.2f}")


    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model , model_path)
    logger.info(f"Model Saved to : {model_path}")
    

    os.makedirs("artifacts/encoders", exist_ok=True)
    os.makedirs("artifacts/scaler", exist_ok=True)

    joblib.dump(label_encoders["Transaction"], "artifacts/encoders/transaction_encoder.pkl")
    joblib.dump(label_encoders["Furnishing"], "artifacts/encoders/furnishing_encoder.pkl")
    joblib.dump(label_encoders["Possession_Status"], "artifacts/encoders/possession_status_encoder.pkl")

    joblib.dump(scaler, "artifacts/scaler/minmax_scaler.pkl")


    mlflow.set_experiment("real_estate_price_prediction")
    with mlflow.start_run():
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("f1_score", mae)
        mlflow.log_metric("Accuracy Score", r2)
        
        mlflow.sklearn.log_model(model, "model")




