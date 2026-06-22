from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from smartmoneyconcepts import smc

app = FastAPI()

class OHLCVRequest(BaseModel):
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]

def clean_nan(obj):
    """Recursively replace NaN/Inf with None"""
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    else:
        return obj

@app.post("/fvg")
def get_fvg(data: OHLCVRequest):
    df = pd.DataFrame({
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close
    })
    result = smc.fvg(df)
    if result is None or result.empty:
        return []
    # Convert to dict and clean
    result_dict = result.to_dict(orient="records")
    cleaned = clean_nan(result_dict)
    return cleaned

@app.post("/bos")
def get_bos(data: OHLCVRequest):
    df = pd.DataFrame({
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close
    })
    swings = smc.swing_highs_lows(df)
    if swings is None or swings.empty:
        return []
    result = smc.bos_choch(df, swings)
    if result is None or result.empty:
        return []
    result_dict = result.to_dict(orient="records")
    return clean_nan(result_dict)

@app.post("/swings")
def get_swings(data: OHLCVRequest):
    df = pd.DataFrame({
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close
    })
    result = smc.swing_highs_lows(df)
    if result is None or result.empty:
        return []
    result_dict = result.to_dict(orient="records")
    return clean_nan(result_dict)

@app.get("/")
def root():
    return {"message": "SMC API is running"}
