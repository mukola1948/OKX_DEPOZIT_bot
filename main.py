# ============================================================
# main.py
# OKX Deposit Alert Bot (INFORMATIONAL)
# Виправлено логіку надсилання повідомлень для Telegram
# ============================================================

from datetime import datetime, time, timedelta
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_percent, calc_new_d_past
from formatter import build_message
import requests

# ------------------------------------------------------------
# Часи контрольних повідомлень (3 рази на день)
# ------------------------------------------------------------
HEARTBEAT_TIMES = [
    time(7, 30),
    time(14, 30),
    time(21, 30),
]

# Поріг відсотка зміни для додаткового повідомлення
PERCENT_THRESHOLD = 5.0

# ------------------------------------------------------------
# Відправка повідомлення в Telegram
# ------------------------------------------------------------
def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text})

# ------------------------------------------------------------
# Головна функція
# ------------------------------------------------------------
def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()
    run_id = now.strftime("%Y-%m-%dT%H:%M")

    # Не обробляємо повторно один і той самий запуск
    if state.get("last_run_id") == run_id:
        return

    # Отримуємо поточний баланс USDT
    d_cur = get_balance_usdt()
    if d_cur is None:
        return

    # Ініціалізація стану для першого запуску
    if state.get("day_index") is None:
        state.update({
            "day_index": today,
            "days_count": 0,
            "measure_count": 0,
            "d_past": d_cur,
            "avg_today": d_cur,
            "last_heartbeat_times": {}
        })

    # Новий день — обчислюємо накопичувальне середнє
    if state.get("day_index") != today:
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

    # Оновлення середнього поточного дня
    state["measure_count"] += 1
    n = state["measure_count"]
    prev_avg = state["avg_today"]
    state["avg_today"] = ((prev_avg * (n - 1)) + d_cur) / n

    # Обчислення відсоткової зміни від минулого дня
    percent = calc_percent(d_cur, state["d_past"])

    # ------------------------------------------------------------
    # Надсилаємо повідомлення лише якщо перевищено поріг
    # ------------------------------------------------------------
    if abs(percent) >= PERCENT_THRESHOLD and not state.get("last_percent_sent") == run_id:
        send_telegram(build_message(
            d_cur,
            state["avg_today"],
            state["d_past"],
            percent,
            n_measures=n,
            d_days=state["days_count"],
            dt=now
        ))
        # Запам'ятовуємо, що повідомлення за порогом вже надіслано для цього запуску
        state["last_percent_sent"] = run_id

    # ------------------------------------------------------------
    # Контрольні повідомлення за графіком (3 рази на день)
    # Надсилаємо лише один раз за час hb
    # ------------------------------------------------------------
    for hb in HEARTBEAT_TIMES:
        hb_dt = datetime.combine(now.date(), hb, tzinfo=TZ)
        last_sent_raw = state["last_heartbeat_times"].get(str(hb))
        last_sent = datetime.fromisoformat(last_sent_raw) if last_sent_raw else None

        if now >= hb_dt and (last_sent is None or (now - last_sent) >= timedelta(minutes=1)):
            send_telegram(build_message(
                d_cur,
                state["avg_today"],
                state["d_past"],
                percent,
                n_measures=n,
                d_days=state["days_count"],
                dt=now
            ))
            state["last_heartbeat_times"][str(hb)] = now.isoformat()

    # ------------------------------------------------------------
    # Зберігаємо останній запуск
    # ------------------------------------------------------------
    state["last_run_id"] = run_id
    save_state(state)


if __name__ == "__main__":
    main()
