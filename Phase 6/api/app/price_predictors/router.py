import pandas as pd
from fastapi import status
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .settings import TRAINING_ROW_INSERTION_FILE_PATH, ORIGINAL_DATASET_FILE_PATH, REQUIRED_COLUMNS
from .views import lr_predict, xgb_predict, mlp_predict, retrain
from .data_types import LABEL_MAPPINGS, CarFeaturesWithPrice, CarFeatures, PricePredictionResult, RetrainedModelsResult, ModelMetrics


PredictorRouter = APIRouter()


@PredictorRouter.post("/price")
async def get_price_predictions(car_features: CarFeatures) -> PricePredictionResult:
    if car_features.fuel_type == 9:
        pass

    lr_prediction = lr_predict(car_features)
    xgb_prediction = xgb_predict(car_features)
    mlp_prediction = mlp_predict(car_features)
    return PricePredictionResult(
        lr_prediction=lr_prediction,
        xgb_prediction=xgb_prediction,
        mlp_prediction=mlp_prediction)

@PredictorRouter.get("/label_mappings")
async def get_label_mappings():
    return JSONResponse(LABEL_MAPPINGS)


@PredictorRouter.post("/insert_row", status_code=status.HTTP_201_CREATED)
async def add_training_row(car_features: CarFeaturesWithPrice):
    parsed_data = dict(car_features)
    # Create a DataFrame from the parsed input
    new_row = pd.DataFrame([parsed_data], columns=REQUIRED_COLUMNS)

    try:
        # Try loading the existing CSV
        df_existing = pd.read_csv(TRAINING_ROW_INSERTION_FILE_PATH, index_col=False)
    except FileNotFoundError:
        # If file does not exist, create empty DataFrame
        df_existing = pd.DataFrame(columns=REQUIRED_COLUMNS)
    
    # Concatenate the old data with the new row
    df_final = pd.concat([df_existing, new_row])

    # Save back to CSV
    df_final.to_csv(TRAINING_ROW_INSERTION_FILE_PATH, index=False)

    return JSONResponse({"message": "Row inserted successfully."})



##############################################################################
# Under construction. Caution this might not be safe 
##############################################################################
# TODO: Properly test and implement this so that:
#  - new models are stored along side the previous ones
#  - choose between which trained model to use. (maybe versioning will be useful)
#  - Schedule retraining at midnight (maybe)
@PredictorRouter.post("/__retrain_models__", response_model=RetrainedModelsResult)
async def retrain_models() -> ModelMetrics:
    """Under construction. **Caution:** this is not safe it will overwrite existing models both in memory and on disk"""
    res = retrain([ORIGINAL_DATASET_FILE_PATH, TRAINING_ROW_INSERTION_FILE_PATH])
    return res['metrics']
