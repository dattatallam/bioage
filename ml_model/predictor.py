"""Loads the trained XGBoost model and predicts biological age."""
import os, pickle
import numpy as np, pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biological_age_xgboost_clean.pkl")

with open(MODEL_PATH, "rb") as f:
    _obj = pickle.load(f)
if isinstance(_obj, dict):
    MODEL, FEATURES = _obj["model"], list(_obj["features"])
else:
    MODEL = _obj
    _names = getattr(_obj, "feature_names_in_", None)
    FEATURES = list(_names) if _names is not None else list(_obj.get_booster().feature_names)


def predict_age(given: dict) -> float:
    """given = {NHANES_code: value}. Migilina features empty (NaN) ga teesukuntayi."""
    row = {f: np.nan for f in FEATURES}
    if "BMXHT" in given and "BMXWT" in given:
        given = dict(given, BMXBMI=round(given["BMXWT"] / (given["BMXHT"] / 100) ** 2, 1))
    row.update({k: v for k, v in given.items() if k in row})
    X = pd.DataFrame([row]).reindex(columns=FEATURES).astype(float)
    return round(float(MODEL.predict(X)[0]), 1)
