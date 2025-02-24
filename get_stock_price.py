import yfinance as yf

def get_current_stock_price(symbol):
    stock = yf.Ticker(symbol)
    todays_data = stock.history(period='1d')    
    return round(todays_data['Close'].iloc[0], 2)

def get_dma_20(symbol) -> float:
    stock = yf.Ticker(symbol)
    history_data = stock.history(period='60d')
    dma_20 = history_data['Close'].rolling(window=20).mean().iloc[-1]
    return round(dma_20, 2)


symbol = 'AAPL'
current_price = get_current_stock_price(symbol)
dma_20 = get_dma_20(symbol)
print(f"The current stock price of {symbol} is: ${current_price}")
print(f"The 20-day moving average of {symbol} is: ${dma_20}")
