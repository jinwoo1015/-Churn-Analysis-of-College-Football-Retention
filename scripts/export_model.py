"""One-off: export transfer_model.pkl to version-independent files in model/.

Run in an environment with the versions the pickle was trained with
(scikit-learn==1.6.1, xgboost==2.1.4, imbalanced-learn==0.13.0, Python 3.12):
    python scripts/export_model.py
The app only needs xgboost, numpy and pandas afterwards.
"""
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pipe = pickle.load(open(ROOT / "transfer_model.pkl", "rb"))  # steps: scaler, smote, classifier
(ROOT / "model").mkdir(exist_ok=True)
pipe.named_steps["classifier"].get_booster().save_model(str(ROOT / "model" / "xgb.json"))
scaler = pipe.named_steps["scaler"]
(ROOT / "model" / "scaler.json").write_text(
    json.dumps({"mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist()}, indent=2)
)
