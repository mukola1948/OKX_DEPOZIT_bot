# ============================================================
# formatter.py
# Формування Telegram-повідомлення
#
# УВАГА:
# - ЖОДНОЇ математики
# - ЖОДНИХ тригерів
# - ЛИШЕ вигляд тексту
# ============================================================

def fmt_money(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(d_cur, d_avg, d_past, percent, n_days, dt):
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"
    target_len = len(line1)

    line2 = "Дсереднє(1-n)" + "." * 7 + f"= {fmt_money(d_avg)}"
    line3 = "Дминуле(" + " " * 10 + f"{n_days})= {fmt_money(d_past)}"
    line4 = (
        "OKX"
        + "." * 9
        + dt.strftime("%H:%M")
        + "." * 3
        + dt.strftime("%d-%m-%Y")
    )

    def pad(s):
        return s + " " * (target_len - len(s))

    return "\n".join([
        line1,
        pad(line2),
        pad(line3),
        pad(line4),
    ])
