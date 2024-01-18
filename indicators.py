import talib

def calculate_ema(data, period):
    return talib.EMA(data, timeperiod=period)

def calculate_rsi(data, period):
    return talib.RSI(data, timeperiod=period)

def calculate_macd(data, fastperiod, slowperiod, signalperiod):
    macd, signal, _ = talib.MACD(data, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, signal