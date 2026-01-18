# calculator.py
# Математика (без форматування і Telegram)

def calc_average(values):
    return sum(values) / len(values)

def calc_new_d_past(old, avg, days):
    # накопичувальне середнє за всі дні
    return (old * days + avg) / (days + 1)

def calc_percent(current, past):
    if past == 0:
        return 0.0
    return (current - past) / past * 100
