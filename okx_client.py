# okx_client.py
# Отримання балансу з OKX (READ ONLY)

import time
import hmac
import base64
import hashlib
import requests
import datetime
from config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

BASE_URL = "https://www.okx.com"


def _headers(method, path, body=""):
    # UTC timestamp у вигляді рядка
    ts = str(time.time())

    # Формування повідомлення для підпису
    msg = ts + method + path + body
    sign = base64.b64encode(
        hmac.new(
            OKX_API_SECRET.encode(),
            msg.encode(),
            hashlib.sha256
        ).digest()
    ).decode()

    # Тимчасова перевірка завантаження ключів (без показу значень)
    print("API_KEY loaded:", bool(OKX_API_KEY))
    print("API_SECRET loaded:", bool(OKX_API_SECRET))
    print("PASSPHRASE loaded:", bool(OKX_PASSPHRASE))

    # Використовуємо timezone-aware UTC datetime
    current_utc = datetime.datetime.now(datetime.timezone.utc)
    print("Timestamp sent:", ts)
    print("Current UTC:", current_utc.isoformat())

    return {
        "OK-ACCESS-KEY": OKX_API_KEY,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": ts,
        "OK-ACCESS-PASSPHRASE": OKX_PASSPHRASE,
        "Content-Type": "application/json"
    }


def get_balance_usdt():
    path = "/api/v5/account/balance"
    # GET запит з body="" для правильного підпису
    r = requests.get(BASE_URL + path, headers=_headers("GET", path, ""), timeout=10)
    r.raise_for_status()
    data = r.json()

    total = 0.0
    for acc in data["data"][0]["details"]:
        if acc["ccy"] == "USDT":
            total += float(acc["eq"])
    return total
