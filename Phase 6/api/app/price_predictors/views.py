import json
import joblib
import pandas as pd
import xgboost as xgb
import tensorflow as tf
from fastapi import HTTPException

from .data_types import CarFeatures, PricePredictionResult

from . import STANDARD_SCALER, XGB_MODEL, MLP_MODEL, LR_MODEL
from .settings import REQUIRED_COLUMNS, FEATURE_COLUMNS, TARGET_COLUMNS
from .settings import SCALER_PATH, XGB_MODEL_PATH, MLP_MODEL_PATH, LR_MODEL_PATH, FEATURE_COLUMNS_PATH, COMBINED_DATASET_LATEST_FILE_PATH




def validate_and_prepare_input(input_data: CarFeatures) -> pd.DataFrame:
	"""Convert input data to properly formatted DataFrame"""
	try:
		# Create DataFrame and ensure correct column order
		input_df = pd.DataFrame(input_data, columns=FEATURE_COLUMNS, index=[0])

		# Fill any missing columns with 0 for now (or appropriate default later)
		input_df = input_df.fillna(0)

		return input_df
	except Exception as e:
		raise ValueError(f"Input validation failed: {str(e)}")



def lr_predict(car_features: CarFeatures):
	"""Linear Regression prediction endpoint"""
	try:
		parsed_data = dict(car_features)
		input_df = validate_and_prepare_input(parsed_data)
		scaled_data = STANDARD_SCALER.transform(input_df)

		prediction = LR_MODEL.predict(scaled_data)
		# return prediction
		prediction_value = prediction[0]
		return prediction_value
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

def xgb_predict(car_features: CarFeatures):
	"""XGBoost prediction endpoint"""
	try:
		parsed_data = dict(car_features)
		input_df = validate_and_prepare_input(parsed_data)
		scaled_df = STANDARD_SCALER.transform(input_df)

		prediction = XGB_MODEL.predict(scaled_df)
		# return prediction
		prediction_value = prediction[0]
		return prediction_value
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

def mlp_predict(car_features: CarFeatures):
	"""Neural Network prediction endpoint"""
	try:
		parsed_data = dict(car_features)
		input_df = validate_and_prepare_input(parsed_data)
		scaled_data = STANDARD_SCALER.transform(input_df)
		prediction = MLP_MODEL.predict(scaled_data, verbose=0)
		# return prediction
		prediction_value = prediction[0][0]
		return prediction_value
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))






############################################################################################
# Model retraining functions
# can be put in a separate script to schedule using `systemd` or `crontab`
############################################################################################
import json
import joblib
import pandas as pd
import xgboost as xgb

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error, mean_squared_error

# MLP model requirements
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Dropout
from tensorflow.keras.mixed_precision import set_global_policy
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
set_global_policy('mixed_float16')  # Enable mixed precision for faster training on GPU
import tensorflow as tf


def evaluate_model(y_true, y_pred):
	return {
		"mse": mean_squared_error(y_true, y_pred),
		"mae": mean_absolute_error(y_true, y_pred),
		"rmse": root_mean_squared_error(y_true, y_pred),
		"r2": r2_score(y_true, y_pred)
	}

def retrain(data_files=[],
			save_models=True, 
			update_models_in_memory=True, 
			save_combined_dataset=True,
			train_mlp=True,
):
	loaded_dfs = []
	for file in data_files:
		df = pd.read_csv(file)
		
		# Check for missing columns
		missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
		if len(missing_columns)>0:
			raise ValueError(f"File: {file} is missing {missing_columns} required columns")
		
		# cleanup extra columns
		extra_columns = set(df.columns) - set(REQUIRED_COLUMNS)
		df.drop(columns=extra_columns, inplace=True)
		
		# add to loaded dataframes
		loaded_dfs.append(df)


	# combine the loaded dataframes
	combined_df = pd.concat(loaded_dfs, axis=0)
	combined_df.dropna(inplace=True)
	combined_df.reset_index()
	# print(combined_df.isna.sum()) # debug
	 

	# split data for training and testing
	X, y = combined_df[FEATURE_COLUMNS], combined_df[TARGET_COLUMNS]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=31)

	# scale data	
	std_scaler = StandardScaler()
	X_train_scaled = std_scaler.fit_transform(X_train)
	X_test_scaled = std_scaler.transform(X_test)


	# train LR model
	lr_model = LinearRegression()
	lr_model.fit(X_train_scaled, y_train)
	# evaluate model
	y_pred_lr = lr_model.predict(X_test_scaled)
	lr_metrics = evaluate_model(y_test, y_pred_lr)


	# train XGB_model
	xgb_model = xgb.XGBRegressor(
		n_estimators=512,
		max_depth=24,
		max_leaves=800,
		learning_rate=0.125,
		gamma=0.005,
		random_state=31
	)
	xgb_model.fit(X_train, y_train)
	# evaluate model
	y_pred_xgb = xgb_model.predict(X_test)
	xgb_metrics = evaluate_model(y_test, y_pred_xgb)


	if train_mlp:
		# Prepare MLP model
		assert X_train_scaled.shape[0] == y_train.shape[0], "Check size of X_train and y_train gap!"
		assert X_test_scaled.shape[0] == y_test.shape[0], "Check size of X_test and y_test gap!"
		# Best model 
		mlp_model = Sequential([
			Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
			Dropout(0.3),  # Increase dropout to reduce overfitting
			Dense(32, activation='relu'),
			Dropout(0.3),
			Dense(1)
		])
		
		mlp_model.compile(
			optimizer=Adam(learning_rate=0.001),
			loss=tf.keras.losses.Huber(),
			metrics=['mae']
		)

		# Callbacks: EarlyStopping and ReduceLROnPlateau
		early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
		reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)

		# Train the MLP model
		mlp_model.fit(
			X_train_scaled, y_train,
			validation_split=0.2,
			epochs=5,
			batch_size=512,
			callbacks=[early_stopping, reduce_lr],
			verbose=True
		)

		# Evaluate model
		y_pred_mlp = mlp_model.predict(X_test_scaled)
		mlp_metrics = evaluate_model(y_test, y_pred_mlp)
	else:
		mlp_model = None
		mlp_metrics = {
			"mse": 0,
			"mae": 0,
			"rmse": 0,
			"r2": 0,
		}


	if update_models_in_memory:
		# update global variables
		global STANDARD_SCALER, LR_MODEL, MLP_MODEL, XGB_MODEL
		STANDARD_SCALER = std_scaler
		LR_MODEL = lr_model
		MLP_MODEL = mlp_model
		XGB_MODEL = xgb_model
	
	if save_models:
		# Save files
		xgb_model.save_model(XGB_MODEL_PATH)
		if train_mlp:
			mlp_model.save(MLP_MODEL_PATH)
		joblib.dump(lr_model, LR_MODEL_PATH)
		joblib.dump(std_scaler, SCALER_PATH)
		with open(FEATURE_COLUMNS_PATH, 'w+') as f:
			json.dump(list(X_train.columns), fp=f)
	
	if save_combined_dataset:
		combined_df.to_csv(COMBINED_DATASET_LATEST_FILE_PATH, columns=REQUIRED_COLUMNS, index=False)
	
	return {
		"models": {
			"linear_regression": lr_model,
			"xgboost": xgb_model,
			"mlp": mlp_model
		},
		"metrics": {
			"linear_regression": lr_metrics,
			"xgboost": xgb_metrics,
			"mlp": mlp_metrics
		}
	}

