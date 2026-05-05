import yfinance as yf
info = yf.Ticker("6981.T").info
print("Summary:", info.get('longBusinessSummary')[:100] if info.get('longBusinessSummary') else "None")
