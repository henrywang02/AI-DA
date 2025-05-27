import os; os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
import json
import joblib
import xgboost as xgb
import tensorflow as tf
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from .settings import *


# Check for model files existence
for file in REQUIRED_FILES:
    if not file.exists():
        raise RuntimeError(f"Required file {file} not found. Please check your trained_models directory.")

# Load models and assets
try:
    if "FEATURE_COLUMNS_PATH" not in globals():
        # Load feature names and order
        with open(FEATURE_COLUMNS_PATH, 'r') as f:
            FEATURE_COLUMNS = json.load(f)
    
    XGB_MODEL = xgb.XGBRegressor()
    # Load models
    XGB_MODEL.load_model(XGB_MODEL_PATH)
    LR_MODEL: LinearRegression = joblib.load(LR_MODEL_PATH)
    MLP_MODEL = tf.keras.models.load_model(MLP_MODEL_PATH)
    
    STANDARD_SCALER: StandardScaler = joblib.load(SCALER_PATH)

except Exception as e:
    raise RuntimeError(f"Error loading models: {str(e)}")
