# ============================================================
# main.py
# OKX Deposit Alert Bot
#
# УВАГА:
# - Логіка тригерів НЕ змінена
# - Додано observation log (OBSERVATION_LOG.md)
# - Оформлення повідомлень: ЗВИЧАЙНИЙ TEXT
# - Довжина рядків 2–4 = рядку 1
# ============================================================

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import (
    calc_average,
    calc_new_d_past,
    calc_percent
)
from formatter import build_message
import requests

HEARTBEAT_TIME = time(7, 30)
PERCENT_THRESHOLD = 5.0


# ------------------------------------------------------------
# Надсилання повідомлення в Telegram (PLAIN TEXT)
# ------------------------------------------------------------
def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TG_CHAT_ID,
        "text": text
    })


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # --------------------------------------------------------
    # ПЕРШИЙ ЗАПУСК
    # --------------------------------------------------------
    if state["day_index"] is None:
        state["day_index"] = today
        state["d_past"] = d_cur
        state["days_count"] = 1

    # --------------------------------------------------------
    # НОВИЙ ДЕНЬ
    # --------------------------------------------------------
    if state["day_index"] != today:
        d_avg_yesterday = calc_average(state["values_today"])
        state["d_past"] = calc_new_d_past(
            state["d_past"],
            d_avg_yesterday,
            state["days_count"]
        )
        state["days_count"] += 1
        state["values_today"] = []
        state["day_index"] = today
        state["last_heartbeat_date"] = None

    # --------------------------------------------------------
    # ПОТОЧНЕ ВИМІРЮВАННЯ
    # --------------------------------------------------------
    state["values_today"].append(d_cur)

    d_avg_today = calc_average(state["values_today"])
    percent = calc_percent(d_cur, state["d_past"])

    # --------------------------------------------------------
    # ТРИГЕР: % ЗМІНА
    # --------------------------------------------------------
    if abs(percent) >= PERCENT_THRESHOLD:
        msg = build_message(
            d_cur,
            d_avg_today,
            state["d_past"],
            percent,
            state["days_count"],
            now
        )
        send_telegram(msg)

    # --------------------------------------------------------
    # ТРИГЕР: HEARTBEAT
    # --------------------------------------------------------
    if now.time() >= HEARTBEAT_TIME and state["last_heartbeat_date"] != today:
        msg = build_message(
            d_cur,
            d_avg_today,
            state["d_past"],
            percent,
            state["days_count"],
            now
        )
        send_telegram(msg)
        state["last_heartbeat_date"] = today

    save_state(state)


if __name__ == "__main__":
    main()
