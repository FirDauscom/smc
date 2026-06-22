from fastapi import FastAPI, HTTPException
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

def clean_nan(df):
    """Replace NaN with None for JSON serialization"""
    return df.where(pd.notnull(df), None)

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
    result = clean_nan(result)
    return result.to_dict(orient="records")

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
    result = clean_nan(result)
    return result.to_dict(orient="records")

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
    result = clean_nan(result)
    return result.to_dict(orient="records")

@app.get("/")
def root():
    return {"message": "SMC API is running. Use /fvg, /bos, or /swings endpoints."}
