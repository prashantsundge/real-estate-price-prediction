# src/api/main.py
from fastapi import FastAPI
from src.models.schemas import PropertyFeatures
from src.models.predict_model import predict_price
from src.utils.logger import logger
from src.models.train_model_ensemble import train_ensemble_model

app = FastAPI(title="Real Estate Price Predictor")

@app.get("/")
def read_root():
    return {"message": "Real Estate Price Predictor is live. Use /docs to interact."}

@app.post("/predict")
def predict(data: PropertyFeatures):
    logger.info("MODEL PREDICT STARTED...")
    prediction = predict_price(data)
    logger.info("MODEL PREDICT COMPLETED...")
    return {"predicted_price": prediction}

train_ensemble_model()

# DO NOT place any route inside a function or block like `if __name__ == "__main__"`
# DO NOT place `logger.info(...)` at the module level if it's unrelated to startup
