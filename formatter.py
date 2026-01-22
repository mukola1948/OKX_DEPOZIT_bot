# ============================================================
# formatter.py
# ФОРМУВАННЯ TELEGRAM-ПОВІДОМЛЕННЯ
#
# ФІЗИЧНО РОЗВЕДЕНО:
# - n_measures_today → тільки Дсереднє
# - D_days           → тільки Дминуле
# ============================================================

def fmt_money(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(
    d_cur: float,
    d_avg_today: float,
    d_past: float,
    percent: float,
    n_measures_today: int,
    D_days: int,
    dt
):
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"
    line2 = f"Дсереднє(1-{n_measures_today:02d}).......= {fmt_money(d_avg_today)}"
    line3 = f"Дминуле({10*' '}{D_days})= {fmt_money(d_past)}"
    line4 = (
        "OKX"
        + "." * 9
        + dt.strftime("%H:%M")
        + "." * 3
        + dt.strftime("%d-%m-%Y")
    )

    target_len = len(line1)

    def pad(s: str) -> str:
        return s + " " * (target_len - len(s))

    return "\n".join(map(pad, [line1, line2, line3, line4]))
