import ccxt
import pandas as pd
import talib

def calculate_ema(data, period):
    return talib.EMA(data, timeperiod=period)

def calculate_rsi(data, period):
    return talib.RSI(data, timeperiod=period)

def calculate_macd(data, fastperiod, slowperiod, signalperiod):
    macd, signal, _ = talib.MACD(data, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, signal
# Binance API anahtarları
api_key = ''
api_secret = ''
symbol = 'ETCUSDT'
timeframe = '1s'
candles_limit = 100
stop_loss_ratio = 0.05  # %5 stop loss oranı
take_profit_ratio = 0.15  # %15 take profit oranı
rsi_period = 14  # RSI periyodu
macd_fast = 12
macd_slow = 26
macd_signal = 9

# Binance bağlantısı oluştur
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Grafik verilerini al
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=candles_limit)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# İndikatörleri hesapla
df['ema_7'] = calculate_ema(df['close'], 7)
df['ema_25'] = calculate_ema(df['close'], 25)
df['rsi'] = calculate_rsi(df['close'], rsi_period)
df['macd'], df['macd_signal'] = calculate_macd(df['close'], macd_fast, macd_slow, macd_signal)

# Ticaret stratejisi
def apply_strategy(row):
    if row['ema_7'] > row['ema_25'] and row['macd'] > row['macd_signal']:
        return 'BUY'
    elif row['ema_7'] < row['ema_25'] and row['macd'] < row['macd_signal']:
        return 'SELL'
    elif row['close'] < (1 - stop_loss_ratio) * row['close']:
        return 'SELL'
    elif row['close'] > (1 + take_profit_ratio) * row['close']:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(apply_strategy, axis=1)

# Alım satım sinyallerini göster
buy_signals = df[df['signal'] == 'BUY']
sell_signals = df[df['signal'] == 'SELL']
hold_signals = df[df['signal'] == 'HOLD']

print(buy_signals)
print(sell_signals)
print(hold_signals)