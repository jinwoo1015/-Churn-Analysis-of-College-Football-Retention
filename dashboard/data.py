"""Data loading and scoring. No Streamlit layout code lives here."""
from pathlib import Path
import json

import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb

ROOT = Path(__file__).resolve().parent.parent
FEATURES = ["Avg_Player_Load_Per_Min", "Season_Max_Velocity", "homeLatitude"]
_JITTER_DEG = 0.04  # spreads players from the same hometown so map dots don't stack


@st.cache_resource
def load_model() -> tuple[xgb.Booster, np.ndarray, np.ndarray]:
    """XGBoost booster plus the scaler it was trained behind (see scripts/export_model.py)."""
    booster = xgb.Booster(model_file=str(ROOT / "model" / "xgb.json"))
    scaler = json.loads((ROOT / "model" / "scaler.json").read_text())
    return booster, np.array(scaler["mean"]), np.array(scaler["scale"])


def predict_risk(df: pd.DataFrame) -> np.ndarray:
    """Transfer probability (0-100) for each row."""
    booster, mean, scale = load_model()
    scaled = (df[FEATURES].to_numpy(dtype=float) - mean) / scale
    return booster.predict(xgb.DMatrix(scaled)) * 100


@st.cache_data
def load_roster() -> pd.DataFrame:
    """Roster scored with the transfer model; `risk` is the 0-100 transfer probability."""
    df = pd.read_csv(ROOT / "chunn_model_data_repo.csv").rename(columns={"Name_x": "name"})
    df["risk"] = predict_risk(df).round(1)
    df["outcome"] = np.where(df["transfer"] == 1, "Transferred", "Stayed")
    df["hometown"] = df["homeCity"] + ", " + df["homeState"]

    rng = np.random.default_rng(7)  # seeded so the map is stable across reruns
    df["lat"] = df["homeLatitude"] + rng.uniform(-_JITTER_DEG, _JITTER_DEG, len(df))
    df["lon"] = df["homeLongitude"] + rng.uniform(-_JITTER_DEG, _JITTER_DEG, len(df))
    return df.sort_values("risk", ascending=False, ignore_index=True)
