# ============================================================
# main.py
# OKX Deposit Alert Bot (INFORMATIONAL)
#
# Логіка:
# - state.json = єдина памʼять
# - Дсереднє — інкрементне
# - Дминуле — фіксується на 00:00
# - formatter — ЛИШЕ вигляд
# ============================================================

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_percent
from formatter import build_message
import requests

HEARTBEAT_TIME = time(7, 30)
PERCENT_THRESHOLD = 5.0


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})


def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()
    run_id = now.strftime("%Y-%m-%dT%H:%M")

    # Guard-flag: цей run вже був
    if state["last_run_id"] == run_id:
        return

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # ---------- ПЕРШИЙ ЗАПУСК ВЗАГАЛІ ----------
    if state["day_index"] is None:
        state.update({
            "day_index": today,
            "days_count": 1,
            "measure_count": 0,
            "d_past": d_cur,
            "avg_today": d_cur,
            "last_heartbeat_date": None
        })

    # ---------- НОВИЙ ДЕНЬ ----------
    if state["day_index"] != today:
        state["d_past"] = state["avg_today"]
        state["days_count"] += 1
        state["measure_count"] = 0
        state["avg_today"] = d_cur
        state["day_index"] = today
        state["last_heartbeat_date"] = None

    # ---------- НОВИЙ ЗАМІР ----------
    state["measure_count"] += 1
    n = state["measure_count"]
    prev_avg = state["avg_today"]
    state["avg_today"] = ((prev_avg * (n - 1)) + d_cur) / n

    percent = calc_percent(d_cur, state["d_past"])

    # ---------- % ТРИГЕР ----------
    if abs(percent) >= PERCENT_THRESHOLD:
        send_telegram(build_message(
            d_cur, state["avg_today"], state["d_past"],
            percent, n, now
        ))

    # ---------- HEARTBEAT ----------
    if now.time() >= HEARTBEAT_TIME and state["last_heartbeat_date"] != today:
        send_telegram(build_message(
            d_cur, state["avg_today"], state["d_past"],
            percent, n, now
        ))
        state["last_heartbeat_date"] = today

    state["last_run_id"] = run_id
    save_state(state)


if __name__ == "__main__":
    main()
