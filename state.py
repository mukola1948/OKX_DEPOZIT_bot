# ============================================================
# state.py
# Persistent state між workflow
# ============================================================

import json
from pathlib import Path

STATE_FILE = Path("state.json")

DEFAULT_STATE = {
    "D_days": 0,                 # завершені дні
    "day_index": None,
    "d_past": None,
    "avg_today": None,
    "n_measures_today": 0,
    "last_heartbeat_date": {},   # <-- ЗАВЖДИ dict
    "last_run_id": None
}

def load_state():
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())

        # 🔧 МІГРАЦІЯ зі старого формату
        if isinstance(state.get("last_heartbeat_date"), str):
            state["last_heartbeat_date"] = {}

        return state

    return DEFAULT_STATE.copy()

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))
