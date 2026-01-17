# config.py
# Центральна конфігурація. Зчитуємо змінні середовища (GitHub Secrets)

import os
from datetime import timezone, timedelta

OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_API_SECRET = os.getenv("OKX_API_SECRET")
OKX_PASSPHRASE = os.getenv("OKX_PASSPHRASE")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# Фіксований часовий пояс UTC+2
TZ = timezone(timedelta(hours=2))
