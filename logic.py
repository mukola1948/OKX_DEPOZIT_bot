"""
logic.py
Розрахунок показників одного виміру
"""

def calculate(curr, prev):
    percent = ((curr - prev) / prev) * 100 if prev else 0
    avg = curr  # один вимір
    return avg, percent
