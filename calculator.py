# ============================================================
# calculator.py
# МАТЕМАТИКА БОТА (БЕЗ TELEGRAM І ФОРМАТУВАННЯ)
#
# - calc_percent     → % зміна від Dминуле
# - calc_new_d_past  → накопичувальне Dминуле за D_days
# ============================================================

def calc_percent(current: float, past: float) -> float:
    if past == 0:
        return 0.0
    return (current - past) / past * 100


def calc_new_d_past(old_d_past: float, day_avg: float, d_days: int) -> float:
    """
    Накопичувальне середнє за ВСІ ЗАВЕРШЕНІ ДНІ
    """
    return (old_d_past * d_days + day_avg) / (d_days + 1)
