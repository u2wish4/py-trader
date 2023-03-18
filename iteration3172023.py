import backtrader as bt
import pandas as pd
import quandl
import yfinance as yf

quandl.ApiConfig.api_key = 'Ue5ZXwiprG4dVywqsSxf' # replace with your Quandl API key

def get_stock_price(ticker_symbol):
    # code to access and return the current price of the stock 
    ticker_data = yf.Ticker(ticker_symbol) # create a Ticker object
    today_data = ticker_data.history(period="1d") # get today's data as a pandas DataFrame
    price = today_data["Close"][0] # get the closing price of today
    return price

class SimpleStrategy(bt.Strategy):
    
    def __init__(self):
        self.data_close = self.datas[0].close
        self.sma20 = bt.indicators.SimpleMovingAverage(self.datas[0], period=20)
        self.sma50 = bt.indicators.SimpleMovingAverage(self.datas[0], period=50)
        
    def next(self):
        if self.sma20 > self.sma50:  # If the 20-day moving average is above the 50-day moving average
            self.buy()  # Buy one share
        elif self.sma20 < self.sma50:  # If the 20-day moving average is below the 50-day moving average
            self.sell()  # Sell all shares
        
cerebro = bt.Cerebro()

ticker_symbol = input("Enter the stock symbol: ") # ask for user input
data = bt.feeds.PandasData(dataname=quandl.get('WIKI/' + ticker_symbol, start_date='2016-01-01', end_date='2021-12-31')) # use user input in quandl.get function
current_price = get_stock_price(ticker_symbol) # call the function with user input
print(current_price) # print

cerebro.adddata(data)
cerebro.addstrategy(SimpleStrategy)

cerebro.broker.setcash(10000)
cerebro.broker.setcommission(commission=0.001)

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

