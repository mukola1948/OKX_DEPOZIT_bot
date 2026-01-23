# ============================================================
# formatter.py
# Формування Telegram-повідомлення (PLAIN TEXT)
# ============================================================

def fmt_money(v: float) -> str:
    """
    Форматування чисел у вигляді 1 234 567
    """
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(
    d_cur: float,
    d_avg_today: float,
    d_past: float,
    percent: float,
    n_measures: int,   # кількість замірів сьогодні
    d_days: int,       # кількість завершених днів
    dt
) -> str:
    """
    Формує багаторядкове повідомлення для Telegram
    """
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"
    line2 = f"Дсереднє(1-{n_measures:02d}).....= {fmt_money(d_avg_today)}"
    line3 = f"Дминуле({12*' '}{d_days})= {fmt_money(d_past)}"
    line4 = (
        "OKX"
        + "." * 2
        + dt.strftime("%H:%M")
        + "." * 2
        + dt.strftime("%d-%m-%Y")
    )

    target_len = len(line1)

    def pad(s):
        return s + " " * (target_len - len(s))

    return "\n".join(map(pad, [line1, line2, line3, line4]))
