# ===============================================
# main.py
# OKX Deposit Monitor Bot
# Оновлено: додано ведення OBSERVATION_LOG та
# markdown-форматування для Telegram
# ===============================================

from datetime import datetime, time
from config import TZ, TG_BOT_TOKEN, TG_CHAT_ID
from okx_client import get_balance_usdt
from state import load_state, save_state
from calculator import calc_average, calc_new_d_past, calc_percent
import requests

HEARTBEAT_TIME = time(7, 30)   # 07:30
PERCENT_THRESHOLD = 5.0        # 5 %

def send_telegram(text):
    """Відправка повідомлення в Telegram з markdown-форматуванням і моноширинним шрифтом."""
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TG_CHAT_ID,
        "text": f"```\n{text}\n```",
        "parse_mode": "Markdown"
    })

def build_message(d_cur, d_avg, d_past, percent, n, dt):
    """Формування повідомлення з вирівнюванням по моноширинному шрифту для Telegram.
    Логіка пробілів і крапок для точного візуального шаблону.
    """
    sign = "+" if percent >= 0 else "-"
    percent = abs(percent)

    # рядки повідомлення
    line1 = f"Дпоточне({sign} {percent:.1f} %)= {int(d_cur):,}".replace(",", " ")
    line2 = f"Дсер(1-{n:02d})..................= {int(d_avg):,}".replace(",", " ")
    # 12 пробілів після дужки, для N може збільшуватися
    line3 = f"Дминуле({ ' ' * (12 - len(str(n))) }{n})= {int(d_past):,}".replace(",", " ")
    line4 = f"OKX.........{dt.strftime('%H:%M')}...{dt.strftime('%d-%m-%Y')}"

    return f"{line1}\n{line2}\n{line3}\n{line4}"

def main():
    state = load_state()
    now = datetime.now(TZ)
    today = now.date().isoformat()

    d_cur = get_balance_usdt()
    if d_cur is None:
        return  # якщо не вдалося отримати баланс, завершуємо без помилки

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

    # --- ТРИГЕР A: зміна ≥5% ---
    if abs(percent) >= PERCENT_THRESHOLD:
        msg = build_message(
            d_cur, d_avg, state["d_past"],
            percent, len(state["values_today"]), now
        )
        send_telegram(msg)

    # --- ТРИГЕР B: heartbeat 07:30 ---
    if now.time() >= HEARTBEAT_TIME and state["last_heartbeat_date"] != today:
        msg = build_message(
            d_cur, d_avg, state["d_past"],
            percent, len(state["values_today"]), now
        )
        send_telegram(msg)
        state["last_heartbeat_date"] = today

    save_state(state)

if __name__ == "__main__":
    main()
