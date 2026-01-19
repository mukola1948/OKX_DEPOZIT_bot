# ============================================================
# calculator.py
# Математика без форматування та Telegram
# ============================================================

def calc_average(values: list[float]) -> float:
    """
    Обчислення середнього значення зі списку чисел.
    """
    return sum(values) / len(values)


def calc_percent(current: float, past: float) -> float:
    """
    Обчислення відсоткової зміни від попереднього значення.
    """
    if past == 0:
        return 0.0
    return (current - past) / past * 100


def calc_new_d_past(old_d_past: float, day_avg: float, days_count: int) -> float:
    """
    Накопичувальне середнє за всі дні роботи бота.
    """
    return (old_d_past * days_count + day_avg) / (days_count + 1)
