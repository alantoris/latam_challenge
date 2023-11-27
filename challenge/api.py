from pydantic import BaseModel, BaseConfig, constr, validator
from fastapi import FastAPI, HTTPException

import joblib
import numpy as np

from .utils import get_allowed_airlines, prepare_data

app = FastAPI()


class Item(BaseModel):
    """
    Item class to represent the list of flights received
    """
    flights: list[dict]


class FlightItem(BaseModel):
    """
    Item class to represent each flight received
    """
    OPERA: str
    MES: int
    TIPOVUELO: constr(min_length=1, max_length=1, regex=r'^[IN]$')

    @validator("MES")
    def validate_month(cls, month):
        if not (1 <= month <= 12):
            raise ValueError("Month must be an integer between 1 and 12")
        return month

    @validator("OPERA")
    def validate_name(cls, opera):
        allowed_values = get_allowed_airlines()
        if opera not in allowed_values:
            raise ValueError(f"Invalid value.")
        return opera


model = joblib.load("./challenge/xgb_model.joblib")

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(item: Item) -> dict:
    try:
        validated_features = [FlightItem(**flight) for flight in item.flights]
        input_data = np.array([prepare_data(f) for f in validated_features])
        prediction = model.predict(input_data)
        prediction = [1 if y_pred > 0.5 else 0 for y_pred in prediction]
        return {"predict": prediction}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
