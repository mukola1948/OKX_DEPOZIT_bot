# ============================================================
# formatter.py
# Формування Telegram-повідомлення у plain-text
#
# УВАГА:
# - ЖОДНОЇ математики
# - ЖОДНИХ тригерів
# - ЛИШЕ вигляд тексту
# - Усунута помилка 1-n
# ============================================================

def fmt_money(v: float) -> str:
    """
    Форматування чисел із пробілами як роздільник тисяч.
    1268 -> '1 268'
    12345 -> '12 345'
    """
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(d_cur, d_avg, d_past, percent, n_days, dt):
    """
    Формує plain-text повідомлення для Telegram.
    Забезпечує однакову довжину рядків.
    """

    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    # -------- рядок 1 --------
    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"
    target_len = len(line1)

    # -------- рядок 2 --------
    # Дсереднє(1-XX) замість старого 1-n
    line2 = f"Дсереднє(1-{n_days:02d})" + "." * 7 + f"= {fmt_money(d_avg)}"

    # -------- рядок 3 --------
    line3 = f"Дминуле({10*' '}{n_days})= {fmt_money(d_past)}"

    # -------- рядок 4 --------
    line4 = (
        "OKX"
        + "." * 9
        + dt.strftime("%H:%M")
        + "." * 3
        + dt.strftime("%d-%m-%Y")
    )

    # добивання пробілами до довжини рядка 1
    def pad(s):
        return s + " " * (target_len - len(s))

    return "\n".join([
        line1,
        pad(line2),
        pad(line3),
        pad(line4),
    ])
