# ============================================================
# calculator.py
# Чиста математика (без форматування і Telegram)
# ============================================================

def calc_percent(current: float, past: float) -> float:
    if past == 0:
        return 0.0
    return (current - past) / past * 100


def calc_new_d_past(old_d_past: float, day_avg: float, D_days: int) -> float:
    """
    Накопичувальне середнє за всі завершені дні.
    D_days — КІЛЬКІСТЬ ЗАВЕРШЕНИХ ДНІВ
    """
    return (old_d_past * D_days + day_avg) / (D_days + 1)
