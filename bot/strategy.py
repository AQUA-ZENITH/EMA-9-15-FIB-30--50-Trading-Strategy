import pandas as pd
from datetime import datetime, timedelta
from bot.kite_client import kite, instrument_map
from bot.config import *
from bot.indicators import calculate_indicators
from bot.helpers import atm_strike
from bot.logger import get_logger

logger = get_logger(__name__)

def option_ltp(symbol):
    quote = kite.quote(f"NFO:{symbol}")
    return quote[f"NFO:{symbol}"]["last_price"]

def run():
    to_dt = datetime.now(IST)
    from_dt = to_dt - timedelta(days=5)

    data = kite.historical_data(
        TOKEN_SPOT, from_dt, to_dt, TIMEFRAME
    )
    df = pd.DataFrame(data)

    if len(df) < MIN_DATA_ROWS:
        return

    df = calculate_indicators(df, COMPRESSION_THRESHOLD)
    candle = df.iloc[-2]

    score = 0
    if abs(candle.ema9 - candle.ema15) / candle.close * 100 > EMA_DIVERGENCE_PCT:
        score += 1
    if candle.compression:
        score += 1

    if score < 2:
        return

    strike = atm_strike(candle.close)

    if candle.close > candle.open and candle.ema9 > candle.ema15:
        return f"NIFTY{EXPIRY_TAG}{strike}CE"

    if candle.open > candle.close and candle.ema9 < candle.ema15:
        return f"NIFTY{EXPIRY_TAG}{strike}PE"
