# formatter.py
# Формування Telegram-повідомлення (ТІЛЬКИ ВИГЛЯД)

def fmt_money(v):
    return f"{int(v):,}".replace(",", " ")

def build_message(d_cur, d_avg, d_past, percent, n, dt):
    sign = "+" if percent >= 0 else "-"
    percent = abs(percent)

    return (
f"Дпоточне({sign} {percent:.1f} %)= {fmt_money(d_cur)}\n"
f"Дсер (1-{n:02d})  = {fmt_money(d_avg)}\n"
f"Дминуле ( {n})= {fmt_money(d_past)}\n"
f"OKX{dt.strftime('%H:%M')}.....{dt.strftime('%d-%m-%Y')}"
    )
