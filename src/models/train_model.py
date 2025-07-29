import os 
import pandas as pd 
import joblib
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from src.utils.logger import logger


def train_model(data_path: str = "notebooks/data/processed/clean_df.csv", 
                model_path: str = "artifacts/model/model.pkl"):
    
    logger.info("📦 Loading dataset...")
    df = pd.read_csv(data_path)

    # === 1. Encode categorical columns ===
    label_encoders = {}
    categorical_cols = ["Transaction", "Furnishing", "Possession_Status"]
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        logger.info(f"✅ Encoded: {col}")

    # === 2. Normalize numerical columns ===
    scaler = MinMaxScaler()
    continuous_cols = ["Price per Sqft", "Total Area"]
    df[continuous_cols] = scaler.fit_transform(df[continuous_cols])
    logger.info("✅ Normalized numerical columns.")

    # === 3. Prepare features and target ===
    X = df[["Transaction", "Furnishing", "Bathroom", "Price per Sqft",
            "Total Area", "Covered_parking", "Open_parking", 
            "Possession_Status", "BHK"]]
    y = df["Price_INR_Numeric"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # === 4. Train model ===
    model = LinearRegression()
    model.fit(X_train, y_train)
    logger.info("✅ Linear Regression model trained.")

    # === 5. Evaluate ===
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    logger.info(f"📊 RMSE: {rmse:.2f}")
    logger.info(f"📊 MAE: {mae:.2f}")
    logger.info(f"📊 R2 Score: {r2:.2f}")

    # === 6. Save model ===
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"💾 Model saved to: {model_path}")

    # === 7. Save encoders and scaler ===
    os.makedirs("artifacts/encoders", exist_ok=True)
    os.makedirs("artifacts/scaler", exist_ok=True)

    for col, le in label_encoders.items():
        joblib.dump(le, f"artifacts/encoders/{col.lower()}_encoder.pkl")

    joblib.dump(scaler, "artifacts/scaler/minmax_scaler.pkl")
    logger.info("💾 Encoders and scaler saved.")

    # === 8. MLflow tracking ===
    mlflow.set_experiment("real_estate_price_prediction")
    with mlflow.start_run():
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)
        mlflow.sklearn.log_model(model, "model")
        logger.info("📈 MLflow tracking completed.")


