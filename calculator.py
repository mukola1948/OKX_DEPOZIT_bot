# ============================================
# calculator.py
# Математика без форматування і Telegram
# ============================================

def calc_average(values: list[float]) -> float:
    return sum(values) / len(values)


def calc_percent(current: float, past: float) -> float:
    if past == 0:
        return 0.0
    return (current - past) / past * 100


def calc_new_d_past(old_d_past: float, day_avg: float, days_count: int) -> float:
    """
    Накопичувальне середнє за всі дні.
    """
    return (old_d_past * days_count + day_avg) / (days_count + 1)
