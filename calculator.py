# calculator.py
# Усі математичні розрахунки бота

def calc_average(values):
    """
    Середнє значення за поточний день (Дсер)
    """
    return sum(values) / len(values)


def calc_new_d_past(old, avg, days):
    """
    Розрахунок історичного середнього (Дминуле)

    ЛОГІКА:
    - old  — попереднє Дминуле
    - avg  — Дсер за завершений день
    - days — кількість завершених днів роботи бота

    Формула:
    нове Дминуле = (old * days + avg) / (days + 1)
    """
    return (old * days + avg) / (days + 1)


def calc_percent(current, past):
    """
    Відсоткова зміна між Дпоточне і Дминуле
    """
    if past == 0:
        return 0.0
    return (current - past) / past * 100
