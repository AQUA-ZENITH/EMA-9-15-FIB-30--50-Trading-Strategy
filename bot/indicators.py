import numpy as np

def calculate_indicators(df, compression_threshold):
    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema15"] = df["close"].ewm(span=15).mean()

    df["swing_high"] = df["high"].rolling(15).max()
    df["swing_low"] = df["low"].rolling(15).min()

    swing_range = (df["swing_high"] - df["swing_low"]).replace(0, np.nan)

    df["fib30"] = df["swing_low"] + 0.3 * swing_range
    df["fib50"] = df["swing_low"] + 0.5 * swing_range
    df["fib70"] = df["swing_low"] + 0.7 * swing_range

    df["range"] = df["high"] - df["low"]
    df["avg_range"] = df["range"].rolling(8).mean()
    df["compression"] = df["range"] < (df["avg_range"] * compression_threshold)

    return df
