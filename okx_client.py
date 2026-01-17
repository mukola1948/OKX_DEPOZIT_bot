# okx_client.py
# Отримання балансу з OKX (READ ONLY)

import time
import hmac
import base64
import hashlib
import requests
from config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

BASE_URL = "https://www.okx.com"

def _headers(method, path):
    ts = str(time.time())
    msg = ts + method + path
    sign = base64.b64encode(
        hmac.new(
            OKX_API_SECRET.encode(),
            msg.encode(),
            hashlib.sha256
        ).digest()
    ).decode()

    return {
        "OK-ACCESS-KEY": OKX_API_KEY,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": ts,
        "OK-ACCESS-PASSPHRASE": OKX_PASSPHRASE
    }

def get_balance_usdt():
    path = "/api/v5/account/balance"
    r = requests.get(BASE_URL + path, headers=_headers("GET", path), timeout=10)
    r.raise_for_status()
    data = r.json()

    total = 0.0
    for acc in data["data"][0]["details"]:
        if acc["ccy"] == "USDT":
            total += float(acc["eq"])
    return total
