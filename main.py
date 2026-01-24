# ============================================================
# ФАЙЛ: main.py
# OKX Deposit Alert Bot (INFORMATIONAL)
#
# ОПИС:
# - Запускається через GitHub Actions
# - Надсилає контрольні повідомлення 3 рази на день
# - Надсилає позапланове повідомлення ЛИШЕ при досягненні ПОРОГУ ±5%
# ============================================================

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_percent, calc_new_d_past
from formatter import build_message
import requests

# ------------------------------------------------------------
# Контрольні часи (3 повідомлення на добу)
# ------------------------------------------------------------
HEARTBEAT_TIMES = [
    time(7, 30),
    time(14, 30),
    time(21, 30),
]

# ------------------------------------------------------------
# ПОРОГ зміни у відсотках
# ------------------------------------------------------------
PERCENT_THRESHOLD = 5.0


def send_telegram(text: str):
    """
    Відправка повідомлення в Telegram
    """
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})


def main():
    """
    Головна функція виконання бота
    """
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()

    state.setdefault("heartbeat_sent", {})

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    if state.get("day_index") is None:
        state.update({
            "day_index": today,
            "days_count": 0,
            "measure_count": 0,
            "d_past": d_cur,
            "avg_today": d_cur,
        })

    if state["day_index"] != today:
        state["d_past"] = calc_new_d_past(
            state["d_past"],
            state["avg_today"],
            state["days_count"]
        )
        state["days_count"] += 1
        state["measure_count"] = 0
        state["avg_today"] = d_cur
        state["day_index"] = today
        state["heartbeat_sent"] = {}

    state["measure_count"] += 1
    n = state["measure_count"]
    state["avg_today"] = ((state["avg_today"] * (n - 1)) + d_cur) / n

    percent = calc_percent(d_cur, state["d_past"])

    # --------------------------------------------------------
    # Контрольні повідомлення (07:30 / 14:30 / 21:30)
    # --------------------------------------------------------
    for hb in HEARTBEAT_TIMES:
        key = hb.strftime("%H:%M")
        hb_dt = datetime.combine(now.date(), hb, tzinfo=TZ)

        if now >= hb_dt and not state["heartbeat_sent"].get(key):
            send_telegram(build_message(
                d_cur,
                state["avg_today"],
                state["d_past"],
                percent,
                n,
                state["days_count"],
                now
            ))
            state["heartbeat_sent"][key] = True

    # --------------------------------------------------------
    # Повідомлення по ПОРОГУ ±5%
    # --------------------------------------------------------
    if abs(percent) >= PERCENT_THRESHOLD:
        send_telegram(build_message(
            d_cur,
            state["avg_today"],
            state["d_past"],
            percent,
            n,
            state["days_count"],
            now
        ))

    save_state(state)


if __name__ == "__main__":
    main()
