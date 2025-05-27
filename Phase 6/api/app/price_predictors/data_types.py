import json
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import ClassVar, Dict
from .settings import FEATURE_LABEL_MAPPINGS_PATH

# Load the label mappings
with open(FEATURE_LABEL_MAPPINGS_PATH) as f:
    LABEL_MAPPINGS: Dict[str, Dict[str, int]] = json.load(f)

# Create a reverse mapping (int ➔ str) for decoding
REVERSE_LABEL_MAPPINGS = {
    field: {v: k for k, v in mapping.items()}
    for field, mapping in LABEL_MAPPINGS.items()
}

class CarFeatures(BaseModel):
    """
    Feature columns for car price prediction model
    """

    # Class variable to store mappings
    _label_mappings: ClassVar[Dict[str, Dict[str, int]]] = LABEL_MAPPINGS
    _reverse_label_mappings: ClassVar[Dict[str, Dict[int, str]]] = REVERSE_LABEL_MAPPINGS

    engine_type: int = Field(description="Encoded engine type.")
    fuel_type: int = Field(description="Encoded fuel type.")
    transmission: int = Field(description="Encoded transmission type.")
    body_type: int = Field(description="Encoded body type.")
    has_incidents: int = Field(description="Whether the car has incident records (0/1).")
    wheel_system: int = Field(description="Encoded wheel system type.")
    horsepower: float = Field(description="Engine horsepower.")
    maximum_seating: int = Field(description="Maximum seating capacity.")
    mileage: float = Field(description="Mileage of the car (non-negative).")
    torque: float = Field(description="Engine torque.")
    year: int = Field(description="Manufacturing year of the car.")
    combined_fuel_economy: float = Field(description="Combined fuel economy (mpg).")
    legroom: float = Field(description="Legroom in inches.")
    major_options_count: float = Field(description="Count of major options.")
    size_of_vehicle: float = Field(description="Size of the vehicle in cubic feet.")

    @field_validator('mileage')
    def mileage_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('Mileage must be a non-negative number')
        return value

    @field_validator('year')
    def year_must_be_reasonable(cls, value):
        current_year = datetime.now().year
        if not (1900 <= value <= current_year + 1):
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return value

    @field_validator('engine_type', 'fuel_type', 'transmission', 'body_type', 'has_incidents', 'wheel_system')
    def validate_encoded_fields(cls, value, info):
        field_name = info.field_name
        valid_codes = cls._reverse_label_mappings.get(field_name)
        if valid_codes is None:
            return value  # skip validation if mapping not found
        if value not in valid_codes:
            raise ValueError(f"Invalid code '{value}' for field '{field_name}'. Valid codes are {list(valid_codes.keys())}")
        return value

    @classmethod
    def encode_label(cls, field: str, label: str) -> int:
        """
        Encode a string label to an integer for a given field.
        """
        mapping = cls._label_mappings.get(field)
        if mapping is None:
            raise ValueError(f"No encoding found for field '{field}'.")
        try:
            return mapping[label]
        except KeyError:
            raise ValueError(f"Invalid label '{label}' for field '{field}'. Valid labels are: {list(mapping.keys())}")

    @classmethod
    def decode_label(cls, field: str, code: int) -> str:
        """
        Decode an integer code to a string label for a given field.
        """
        reverse_mapping = cls._reverse_label_mappings.get(field)
        if reverse_mapping is None:
            raise ValueError(f"No decoding found for field '{field}'.")
        try:
            return reverse_mapping[code]
        except KeyError:
            raise ValueError(f"Invalid code '{code}' for field '{field}'. Valid codes are: {list(reverse_mapping.keys())}")

    class Config:
        json_schema_extra = {
            "example": {
                "engine_type": 6,
                "fuel_type": 5,
                "transmission": 0,
                "body_type": 5,
                "has_incidents": 0,
                "wheel_system": 2,
                "horsepower": 177.0,
                "maximum_seating": 5,
                "mileage": 7.0,
                "torque": 200.0,
                "year": 2019,
                "combined_fuel_economy": 25.0,
                "legroom": 76.3,
                "major_options_count": 1.0,
                "size_of_vehicle": 426.6
            }
        }


from typing import Optional

class CarFeaturesWithPrice(CarFeatures):
    """
    Extension of CarFeatures that includes the price field (for training purposes).
    """
    price: float = Field(description="Price of the car (target variable).")
    
    class Config:
        json_schema_extra = {
            "example": {
                "engine_type": 6,
                "fuel_type": 5,
                "transmission": 0,
                "body_type": 5,
                "has_incidents": 0,
                "wheel_system": 2,
                "horsepower": 177.0,
                "maximum_seating": 5,
                "mileage": 7.0,
                "torque": 200.0,
                "year": 2019,
                "combined_fuel_economy": 25.0,
                "legroom": 76.3,
                "major_options_count": 1.0,
                "size_of_vehicle": 426.6,
                "price": 10.532
            }
        }


class ModelMetrics(BaseModel):
    """
    Metrics for each model including RMSE, MAE, and R2 score.
    """
    mse: float
    mae: float
    rmse: float
    r2: float


class RetrainedModelsResult(BaseModel):
    """
    Results after retraining models.
    """
    linear_regression: ModelMetrics
    xgboost: ModelMetrics
    mlp: ModelMetrics



# Pydantic model for the output data structure
class PricePredictionResult(BaseModel):
    lr_prediction: float = Field(description="Predicted price from Linear Regression model. Example: 10.12")
    xgb_prediction: float = Field(description="Predicted price from XGBoost model. Example: 11.09")
    mlp_prediction: float = Field(description="Predicted price from MLP (Neural Network) model. Example: 9.85")
