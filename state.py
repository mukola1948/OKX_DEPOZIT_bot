# ============================================================
# state.py
# Збереження стану між запусками (PERSISTENT STATE)
# ============================================================

import json
from pathlib import Path

STATE_FILE = Path("state.json")

DEFAULT_STATE = {
    "days_count": 0,          # Скільки днів бот працює
    "day_index": None,        # ISO-дата поточного дня
    "d_past": None,           # Dминуле (агреговане)
    "avg_today": None,        # ОСТАННЄ розраховане Дсереднє за день
    "measure_count": 0,       # Лічильник замірів з 00:00 (01..96)
    "last_heartbeat_date": None
}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return DEFAULT_STATE.copy()

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))
