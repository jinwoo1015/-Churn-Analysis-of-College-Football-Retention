"""Score the roster and write docs/data.js for the static dashboard (docs/index.html).

Run from the repo root with the app's requirements installed:
    python scripts/build_site.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dashboard.data import load_roster  # noqa: E402

df = load_roster()
cols = {"name": "name", "position": "pos", "risk": "risk", "outcome": "outcome", "hometown": "town",
        "lat": "lat", "lon": "lon", "Avg_Player_Load_Per_Min": "load", "Season_Max_Velocity": "vel"}
rows = df[list(cols)].rename(columns=cols).round({"lat": 4, "lon": 4, "load": 3, "vel": 2}).to_dict("records")
center = {"lat": round(float(df["lat"].median()), 3), "lon": round(float(df["lon"].median()), 3)}
(ROOT / "docs" / "data.js").write_text(f"window.ROSTER={json.dumps(rows, separators=(',', ':'))};window.MAP_CENTER={json.dumps(center)};\n")
print(f"wrote {len(rows)} players")
