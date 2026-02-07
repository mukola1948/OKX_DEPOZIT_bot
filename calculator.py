# ============================================================
# ФАЙЛ: calculator.py
# НАЗВА: Calculator
#
# ОПИС:
# - Чиста математика
# - Без форматування
# - Без Telegram
# - Дминуле = історичний максимум
# ============================================================

def calc_percent(current: float, past: float) -> float:
    """
    Обчислення відсоткової зміни від Дминуле.
    """
    if past == 0:
        return 0.0
    return (current - past) / past * 100


def calc_new_d_past(old_d_past: float, current: float) -> float:
    """
    Дминуле визначається як історичний максимум:
    якщо Дпоточне більше — оновлюємо,
    інакше залишаємо без змін.
    """
    return max(old_d_past, current)
