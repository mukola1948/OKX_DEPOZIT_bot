# main.py
# Один запуск = один вимір (GitHub Actions)

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_average, calc_new_d_past, calc_percent
from formatter import build_message
import requests

HEARTBEAT_TIME = time(7, 30)   # 07:30
PERCENT_THRESHOLD = 5.0        # 5 %

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})

def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # --- новий день ---
    if state["day_index"] != today:
        if state["values_today"]:
            avg_yesterday = calc_average(state["values_today"])
            if state["d_past"] is not None:
                state["d_past"] = calc_new_d_past(
                    state["d_past"],
                    avg_yesterday,
                    state["days_count"]
                )
                state["days_count"] += 1

        state["values_today"] = []
        state["day_index"] = today
        state["last_heartbeat_date"] = None

        if state["d_past"] is None:
            state["d_past"] = d_cur

    # --- поточний вимір ---
    state["values_today"].append(d_cur)

    d_avg = calc_average(state["values_today"])
    percent = calc_percent(d_cur, state["d_past"])

    # --- ТРИГЕР A: 5 % ---
    if abs(percent) >= PERCENT_THRESHOLD:
        msg = build_message(
            d_cur, d_avg, state["d_past"],
            percent, len(state["values_today"]), now
        )
        send_telegram(msg)

    # --- ТРИГЕР B: heartbeat 07:30 ---
    if (
        now.time() >= HEARTBEAT_TIME and
        state["last_heartbeat_date"] != today
    ):
        msg = build_message(
            d_cur, d_avg, state["d_past"],
            percent, len(state["values_today"]), now
        )
        send_telegram(msg)
        state["last_heartbeat_date"] = today

    save_state(state)

if __name__ == "__main__":
    main()
