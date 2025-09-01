import yfinance as yf

def yahoo_import(tickers, start=None, end=None, interval='1d'):
    data = yf.download(tickers, start=start, end=end, interval=interval, group_by='ticker')
    
    if isinstance(tickers, list):
        adj_close = pd.concat([data[t]['Adj Close'] for t in tickers], axis=1)
        adj_close.columns = tickers
        return adj_close
    else:
        return data['Adj Close']
