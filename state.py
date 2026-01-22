# ============================================================
# state.py
# Persistent state між workflow
# ============================================================

import json
from pathlib import Path

STATE_FILE = Path("state.json")

DEFAULT_STATE = {
    "days_count": 0,
    "day_index": None,
    "d_past": None,
    "avg_today": None,
    "measure_count": 0,
    "last_heartbeat_date": None,
    "last_run_id": None
}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return DEFAULT_STATE.copy()

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))
