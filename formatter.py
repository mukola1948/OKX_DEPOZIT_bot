# ============================================================
# formatter.py
# Формування Telegram-повідомлення у plain-text
# ============================================================

def fmt_money(v: float) -> str:
    """
    Форматування чисел із пробілами як роздільник тисяч.
    """
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(d_cur, d_avg, d_past, percent, n_days, dt):
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"

    line2 = f"Дсереднє(1-{n_days:02d})" + "." * 7 + f"= {fmt_money(d_avg)}"
    line3 = f"Дминуле({10*' '}{n_days})= {fmt_money(d_past)}"

    line4 = (
        "OKX"
        + "." * 9
        + dt.strftime("%H:%M")
        + "." * 3
        + dt.strftime("%d-%m-%Y")
    )

    target_len = len(line1)

    def pad(s):
        return s + " " * (target_len - len(s))

    return "\n".join(map(pad, [line1, line2, line3, line4]))
