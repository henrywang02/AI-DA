from pathlib import Path


CWD = Path(__file__).parent
MODEL_DIR = CWD / "trained_models"
DATASET_DIR = CWD / "datasets"

FEATURE_COLUMNS = [
	"engine_type",
	"fuel_type",
	"transmission",
	"body_type",
	"has_incidents",
	"wheel_system",
	"horsepower",
	"maximum_seating",
	"mileage",
	"torque",
	"year",
	"combined_fuel_economy",
	"legroom",
	"major_options_count",
	"size_of_vehicle",
]
TARGET_COLUMNS = ['price']
REQUIRED_COLUMNS = FEATURE_COLUMNS+TARGET_COLUMNS


# To extend the dataset in future
ORIGINAL_DATASET_FILE_PATH = DATASET_DIR / 'cars_price_prediction_latest.csv'
TRAINING_ROW_INSERTION_FILE_PATH = DATASET_DIR / 'additional_dataset.csv'
COMBINED_DATASET_LATEST_FILE_PATH = DATASET_DIR / 'combined_cars_price_prediction_latest.csv'
if not TRAINING_ROW_INSERTION_FILE_PATH.exists():
	with open(TRAINING_ROW_INSERTION_FILE_PATH, "w+") as f:
		for idx, col in enumerate(REQUIRED_COLUMNS):
			f.write(col)
			if idx!=len(REQUIRED_COLUMNS)-1:
				f.write(",")
		f.write("\n")
	

# Files related the model
FEATURE_COLUMNS_PATH = MODEL_DIR / 'feature_columns.json'
FEATURE_LABEL_MAPPINGS_PATH = MODEL_DIR / 'label_mappings.json'

# Model files
LR_MODEL_PATH = MODEL_DIR / 'lr_price_prediction.pkl'
XGB_MODEL_PATH = MODEL_DIR / 'xgb_price_prediction.ubj'
MLP_MODEL_PATH = MODEL_DIR / 'mlp_price_prediction.keras'
SCALER_PATH = MODEL_DIR / 'scaler_price_prediction.pkl'


#############################################################################
# DO NOT MODIFY
REQUIRED_FILES = [LR_MODEL_PATH, XGB_MODEL_PATH, MLP_MODEL_PATH, SCALER_PATH, FEATURE_COLUMNS_PATH, FEATURE_LABEL_MAPPINGS_PATH]
