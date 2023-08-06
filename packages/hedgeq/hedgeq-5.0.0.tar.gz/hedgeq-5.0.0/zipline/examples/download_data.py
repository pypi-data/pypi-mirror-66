import yfinance as yf

msft = yf.Ticker("SPY")

hist = msft.history(period="max")
hist.to_csv("SPY.csv")

