
import os 
import pandas as pd 
import joblib
import mlflow
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score , mean_squared_error
from sklearn.pipeline import Pipeline
from src.utils.logger import logger
import mlflow.sklearn
from mlflow.models.signature import infer_signature


def train_ensemble_model (data_path: str = "notebooks/data/processed/clean_df.csv", model_path: str = "artifacts/model_ensemble.pkl"):
    logger.info(f"Loading Cleaned Data....")
    df=pd.read_csv(data_path)
    
    X = df[["Transaction", "Furnishing", "Bathroom", "Price per Sqft",
            "Total Area", "Covered_parking", "Open_parking", "Possession_Status", "BHK"]]
    y = df["Price_INR_Numeric"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info("Defining Base regressor ...")
    models = {
        "lr": LinearRegression(),
        "rf":RandomForestRegressor(random_state=42),
        "gbr":GradientBoostingRegressor(random_state=42)

    }

    param_grid = {
        "rf__n_estimators":[100,200],
        "rf__max_depth":[5,10,None],
        "gbr__n_estimators":[100,200],
        "gbr__learning_rate": [0.05, 0.1],

    }

    pipeline = Pipeline([
        ("lr" , models["lr"]),
    ])

    #define Estimators and votingRegressor

    estimators = [
        ("lr", models["lr"]),
        ("rf", models["rf"]),
        ("gbr", models["gbr"])

    ]

    ensemble = VotingRegressor(estimators=estimators)

    logger.info("Tuning GradientBoost and RandomForest...")
    grid =GridSearchCV(estimator=ensemble, param_grid={}, cv=3,n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)

    rmse = mean_squared_error(y_test , y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    signature = infer_signature(X_test, y_pred)

    logger.info(f"RMSE {rmse:.2f} , MAE {mae:.2f} , R2 {r2:.2f}")

    mlflow.set_experiment("real_estate_price_prediction_ensemble")
    with mlflow.start_run():
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)
        mlflow.sklearn.log_model(best_model, "ensemble_model", signature=signature, input_example=X_test.iloc[0:1])


    logger.info("Training Complete with Ensemble Model.")