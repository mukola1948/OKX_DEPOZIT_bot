# calculator.py
# Всі математичні розрахунки

def calc_average(values):
    return sum(values) / len(values)

def calc_new_d_past(old, avg, days):
    return (old * (days - 1) + avg) / days

def calc_percent(current, past):
    if past == 0:
        return 0.0
    return (current - past) / past * 100
