# ============================================================
# ФАЙЛ: main.py
# НАЗВА: OKX Deposit Alert Bot
#
# ОПИС:
# - Основна логіка запуску
# - ALERT: лише при порозі ±5%
# - HEARTBEAT: контрольні повідомлення
# ============================================================

from datetime import datetime, time, timedelta
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_percent, calc_new_d_past
from formatter import build_message
import requests

HEARTBEAT_TIMES = [
    time(7, 30),
    time(14, 30),
    time(21, 30),
]

PERCENT_THRESHOLD = 5.0


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})


def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()
    run_id = now.strftime("%Y-%m-%dT%H:%M")

    if state.get("last_run_id") == run_id:
        return

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
            "last_heartbeat_times": {}
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
        state["last_heartbeat_times"] = {}

    state["measure_count"] += 1
    n = state["measure_count"]

    prev_avg = state["avg_today"]
    state["avg_today"] = ((prev_avg * (n - 1)) + d_cur) / n

    percent = calc_percent(d_cur, state["d_past"])

    alert_sent = False

    # ---------- ALERT ----------
    if abs(percent) >= PERCENT_THRESHOLD:
        send_telegram(build_message(
            d_cur,
            state["avg_today"],
            state["d_past"],
            percent,
            n_measures=n,
            d_days=state["days_count"],
            dt=now
        ))
        alert_sent = True

    # ---------- HEARTBEAT (тільки якщо НЕ БУВ alert) ----------
    if not alert_sent:
        for hb in HEARTBEAT_TIMES:
            hb_dt = datetime.combine(now.date(), hb, tzinfo=TZ)
            last_sent = state["last_heartbeat_times"].get(str(hb))
            if now >= hb_dt and (last_sent is None or now - last_sent >= timedelta(minutes=1)):
                send_telegram(build_message(
                    d_cur,
                    state["avg_today"],
                    state["d_past"],
                    percent,
                    n_measures=n,
                    d_days=state["days_count"],
                    dt=now
                ))
                state["last_heartbeat_times"][str(hb)] = now
                break  # 🔒 лише ОДНЕ heartbeat за запуск

    state["last_run_id"] = run_id
    save_state(state)


if __name__ == "__main__":
    main()
