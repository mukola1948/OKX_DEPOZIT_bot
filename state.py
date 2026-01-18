# state.py
# Збереження стану між запусками (через GitHub Artifacts)

import json
from pathlib import Path

STATE_FILE = Path("state.json")

DEFAULT_STATE = {
    "days_count": 1,
    "d_past": None,
    "day_index": None,
    "values_today": [],
    "last_sent_balance": None,
    "last_heartbeat_date": None
}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return DEFAULT_STATE.copy()

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))
