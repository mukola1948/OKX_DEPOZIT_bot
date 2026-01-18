# main.py
# Один запуск = один вимір (GitHub Actions)

from datetime import datetime
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_average, calc_new_d_past, calc_percent
from formatter import build_message
import requests


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})


def main():
    state = load_state()
    now = datetime.now(TZ)
    day_id = now.date().isoformat()

    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    if "last_sent_balance" not in state:
        state["last_sent_balance"] = None

    # новий день
    if state["day_index"] != day_id:
        if state["values_today"]:
            avg = calc_average(state["values_today"])
            if state["d_past"] is not None:
                state["d_past"] = calc_new_d_past(
                    state["d_past"], avg, state["days_count"]
                )
                state["days_count"] += 1

        state["values_today"] = []
        state["day_index"] = day_id

        if state["d_past"] is None:
            state["d_past"] = d_cur

    state["values_today"].append(d_cur)

    avg = calc_average(state["values_today"])
    percent = calc_percent(d_cur, state["d_past"])

    # ✅ УМОВА 5%
    if abs(percent) >= 5:
        msg = build_message(
            d_cur, avg, state["d_past"], percent,
            len(state["values_today"]), now
        )
        send_telegram(msg)
        state["last_sent_balance"] = d_cur

    save_state(state)


if __name__ == "__main__":
    main()
