def build_message(d_cur, d_avg, d_past, percent, n, dt):
    sign = "+" if percent >= 0 else "-"
    p = abs(percent)

    line1 = f"Дпоточне({sign} {p:0.1f} %)= {fmt_money(d_cur)}"
    L = len(line1)

    line2 = f"Дсереднє(1-{n:02d})" + "." * 7 + f"= {fmt_money(d_avg)}"
    line3 = f"Дминуле({10*' '}{state_days_placeholder})= {fmt_money(d_past)}"
    line4 = "OKX" + "." * 5 + dt.strftime("%H:%M") + "." * 3 + dt.strftime("%d-%m-%Y")

    return "\n".join(s.ljust(L) for s in [line1, line2, line3, line4])
