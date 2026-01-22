# ============================================================
# main.py
# OKX Deposit Alert Bot (INFORMATIONAL)
# ============================================================

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_percent, calc_new_d_past
from formatter import build_message
import requests

HEARTBEAT_TIMES = {
    "07:30": time(7, 30),
    "14:30": time(14, 30),
    "21:30": time(21, 30),
}

PERCENT_THRESHOLD = 5.0


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})


def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()
    run_id = now.strftime("%Y-%m-%dT%H:%M")

    if state["last_run_id"] == run_id:
        return

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # ---------- ПЕРШИЙ ЗАПУСК ----------
    if state["day_index"] is None:
        state.update({
            "day_index": today,
            "D_days": 0,
            "n_measures_today": 0,
            "d_past": d_cur,
            "avg_today": d_cur,
            "last_heartbeat_date": {}
        })

    # ---------- НОВИЙ ДЕНЬ ----------
    if state["day_index"] != today:
        state["d_past"] = calc_new_d_past(
            state["d_past"],
            state["avg_today"],
            state["D_days"]
        )

        state["D_days"] += 1
        state["n_measures_today"] = 0
        state["avg_today"] = d_cur
        state["day_index"] = today
        state["last_heartbeat_date"] = {}

    # ---------- НОВИЙ ВИМІР ----------
    state["n_measures_today"] += 1
    n = state["n_measures_today"]

    prev_avg = state["avg_today"]
    state["avg_today"] = ((prev_avg * (n - 1)) + d_cur) / n

    percent = calc_percent(d_cur, state["d_past"])

    # ---------- % ТРИГЕР ----------
    if abs(percent) >= PERCENT_THRESHOLD:
        send_telegram(build_message(
            d_cur, state["avg_today"], state["d_past"],
            percent, state["D_days"], now
        ))

    # ---------- HEARTBEAT ----------
    for key, t in HEARTBEAT_TIMES.items():
        if now.time() >= t and state["last_heartbeat_date"].get(key) != today:
            send_telegram(build_message(
                d_cur, state["avg_today"], state["d_past"],
                percent, state["D_days"], now
            ))
            state["last_heartbeat_date"][key] = today

    state["last_run_id"] = run_id
    save_state(state)


if __name__ == "__main__":
    main()
