# okx_client.py
# Отримання балансу з OKX (READ ONLY)

import hmac
import base64
import hashlib
import requests
from datetime import datetime, timezone
from config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE

BASE_URL = "https://www.okx.com"


def _utc_timestamp():
    # ISO8601 UTC, як вимагає OKX
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _headers(method: str, path: str, body: str = ""):
    ts = _utc_timestamp()

    prehash = ts + method + path + body
    sign = base64.b64encode(
        hmac.new(
            OKX_API_SECRET.encode("utf-8"),
            prehash.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode()

    return {
        "OK-ACCESS-KEY": OKX_API_KEY,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": ts,
        "OK-ACCESS-PASSPHRASE": OKX_PASSPHRASE,
        "Content-Type": "application/json"
    }


def get_balance_usdt() -> float | None:
    path = "/api/v5/account/balance"

    try:
        r = requests.get(
            BASE_URL + path,
            headers=_headers("GET", path, ""),
            timeout=10
        )
        r.raise_for_status()
    except requests.RequestException:
        # ВАЖЛИВО:
        # ❌ не валимо workflow
        # ✅ даємо main.py вирішувати (Variant A)
        return None

    data = r.json()

    total = 0.0
    for acc in data["data"][0]["details"]:
        if acc["ccy"] == "USDT":
            total += float(acc["eq"])

    return total
