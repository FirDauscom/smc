from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from smartmoneyconcepts import smc

app = FastAPI()

class OHLCVRequest(BaseModel):
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]

@app.post("/fvg")
def get_fvg(data: OHLCVRequest):
    df = pd.DataFrame({
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close
    })
    result = smc.fvg(df)
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
    result = smc.bos_choch(df, swings)
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
    return result.to_dict(orient="records")
