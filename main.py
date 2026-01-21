# ============================================================
# main.py
# OKX Deposit Alert Bot
#
# УВАГА:
# - Логіка тригерів НЕ змінена
# - Стан зберігається у state.json
# - Дсереднє рахується інкрементно
# - formatter відповідає ЛИШЕ за вигляд
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

    # --------------------------------------------------------
    # ПОТОЧНИЙ ЗАПУСК
    # --------------------------------------------------------
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # --------------------------------------------------------
    # ПЕРШИЙ ЗАПУСК ВЗАГАЛІ
    # --------------------------------------------------------
    if state["day_index"] is None:
        state["day_index"] = today
        state["days_count"] = 1
        state["measure_count"] = 0
        state["d_past"] = d_cur
        state["avg_today"] = d_cur
        state["last_heartbeat_date"] = None

    # --------------------------------------------------------
    # НОВИЙ ДЕНЬ (00:00)
    # --------------------------------------------------------
    if state["day_index"] != today:
        state["d_past"] = state["avg_today"]     # фіксуємо минулий день
        state["days_count"] += 1
        state["measure_count"] = 0
        state["avg_today"] = d_cur
        state["day_index"] = today
        state["last_heartbeat_date"] = None

    # --------------------------------------------------------
    # НОВИЙ ЗАМІР (ІНКРЕМЕНТНЕ СЕРЕДНЄ)
    # --------------------------------------------------------
    state["measure_count"] += 1

    n = state["measure_count"]
    prev_avg = state["avg_today"]
    state["avg_today"] = ((prev_avg * (n - 1)) + d_cur) / n

    percent = calc_percent(d_cur, state["d_past"])

    # --------------------------------------------------------
    # ТРИГЕР: % ЗМІНА
    # --------------------------------------------------------
    if abs(percent) >= PERCENT_THRESHOLD:
        msg = build_message(
            d_cur,
            state["avg_today"],
            state["d_past"],
            percent,
            state["measure_count"],   # <-- 01, 02, 03 ... 96
            now
        )
        send_telegram(msg)

    # --------------------------------------------------------
    # ТРИГЕР: HEARTBEAT (07:30)
    # --------------------------------------------------------
    if now.time() >= HEARTBEAT_TIME and state["last_heartbeat_date"] != today:
        msg = build_message(
            d_cur,
            state["avg_today"],
            state["d_past"],
            percent,
            state["measure_count"],
            now
        )
        send_telegram(msg)
        state["last_heartbeat_date"] = today

    save_state(state)


if __name__ == "__main__":
    main()
