from datetime import datetime, time as dt_time, timedelta
from bot.config import IST, STRIKE_STEP
import time

def market_open():
    now = datetime.now(IST)
    if now.weekday() >= 5:
        return False
    return dt_time(9, 15) <= now.time() <= dt_time(15, 30)

def sleep_to_next_candle():
    now = datetime.now(IST)
    next_min = (now.minute // 5 + 1) * 5
    next_run = now.replace(second=2, microsecond=0)

    if next_min >= 60:
        next_run += timedelta(hours=1)
        next_run = next_run.replace(minute=0)
    else:
        next_run = next_run.replace(minute=next_min)

    time.sleep(max(0, (next_run - now).total_seconds()))

def atm_strike(price):
    return round(price / STRIKE_STEP) * STRIKE_STEP
