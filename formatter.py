# ============================================================
# formatter.py
# Формування Telegram-повідомлення
# ============================================================

def fmt_money(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(d_cur, d_avg_today, d_past, percent, D_days, dt):
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"
    line2 = f"Дсереднє(1-{D_days:02d}).....= {fmt_money(d_avg_today)}"
    line3 = f"Дминуле({14*' '}{D_days})= {fmt_money(d_past)}"

    line4 = (
        "OKX....."
        + dt.strftime("%H:%M")
        + "..."
        + dt.strftime("%d-%m-%Y")
    )

    target_len = len(line1)

    def pad(s):
        return s + " " * (target_len - len(s))

    return "\n".join(map(pad, [line1, line2, line3, line4]))
