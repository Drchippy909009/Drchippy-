import ccxt
import pandas as pd
import time

# Configuration
exchange_id = 'bybit'  # Change to your exchange
api_key = 'your_api_key'
api_secret = 'your_api_secret'
symbol = 'BTC/USDT'  # Change to your trading pair
timeframe = '1h'  # Timeframe for the moving averages
short_window = 5
long_window = 20

# Initialize exchange
exchange = getattr(ccxt, exchange_id)({
    'apiKey': api_key,
    'secret': api_secret,
})

def fetch_data(symbol, timeframe, limit):
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

def calculate_moving_averages(df):
    df['short_mavg'] = df['close'].rolling(window=short_window).mean()
    df['long_mavg'] = df['close'].rolling(window=long_window).mean()
    return df

def trade(signal):
    balance = exchange.fetch_balance()
    if signal == "buy":
        amount_to_buy = balance['total']['USDT'] / df['close'].iloc[-1]
        exchange.create_market_buy_order(symbol, amount_to_buy)
        print("Bought:", amount_to_buy)
    elif signal == "sell":
        amount_to_sell = balance['total']['BTC']
        exchange.create_market_sell_order(symbol, amount_to_sell)
        print("Sold:", amount_to_sell)

# Main loop
while True:
    df = fetch_data(symbol, timeframe, limit=long_window + 1)
    df = calculate_moving_averages(df)
    
    if df['short_mavg'].iloc[-2] < df['long_mavg'].iloc[-2] and df['short_mavg'].iloc[-1] > df['long_mavg'].iloc[-1]:
        trade("buy")
    elif df['short_mavg'].iloc[-2] > df['long_mavg'].iloc[-2] and df['short_mavg'].iloc[-1] < df['long_mavg'].iloc[-1]:
        trade("sell")

    time.sleep(3600)  # Sleep for 1 hour before checking again