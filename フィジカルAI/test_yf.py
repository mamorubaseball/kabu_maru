import yfinance as yf
ticker = yf.Ticker("6981.T")
info = ticker.info
print("Market Cap:", info.get('marketCap'))
print("Rev Growth:", info.get('revenueGrowth'))
print("Earn Growth:", info.get('earningsGrowth'))
print("Target Price:", info.get('targetMeanPrice'))
print("Recommendation:", info.get('recommendationKey'))
