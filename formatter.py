# formatter.py
# -------------------------------------------------
# Формування Telegram-повідомлення
# УВАГА:
# - тут НЕМає жодної математики
# - тут НЕМає логіки тригерів
# - тут ЛИШЕ вигляд тексту
# -------------------------------------------------

def fmt_money(v: float) -> str:
    """
    Форматування грошей з пробілом як розділювачем тисяч.
    Приклад:
    1268  -> '1 268'
    12345 -> '12 345'
    """
    return f"{int(round(v)):,}".replace(",", " ")


def build_message(d_cur, d_avg, d_past, percent, n, dt):
    """
    Формує текст повідомлення.
    Повертає ВЖЕ ГОТОВИЙ markdown-блок для Telegram.
    """

    # знак для відсотка
    sign = "+" if percent >= 0 else "-"
    percent_abs = abs(percent)

    # -------- рядок 1 --------
    line1 = f"Дпоточне({sign} {percent_abs:0.1f} %)= {fmt_money(d_cur)}"

    # -------- рядок 2 --------
    # 18 крапок після Дсер(1-n)
    line2 = f"Дсер(1-{n:02d})" + "." * 18 + f"= {fmt_money(d_avg)}"

    # -------- рядок 3 --------
    # Кількість пробілів ПЛАВАЮЧА — залежить від довжини N
    days_str = str(n)
    spaces = " " * max(1, 12 - len(days_str))
    line3 = f"Дминуле({spaces}{days_str})= {fmt_money(d_past)}"

    # -------- рядок 4 --------
    line4 = (
        "OKX"
        + "." * 9
        + dt.strftime("%H:%M")
        + "." * 3
        + dt.strftime("%d-%m-%Y")
    )

    # -------- markdown-блок --------
    # Саме він вмикає моноширинний шрифт у Telegram
    message = "\n".join([line1, line2, line3, line4])

    return f"```\n{message}\n```"
