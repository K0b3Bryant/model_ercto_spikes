import yfinance as yf
import pandas as pd

def yahoo_import(tickers, start=None, end=None, interval='1d'):
    """ Fetch multiple tickers from Yahoo Finance. """
    data = yf.download(tickers, start=start, end=end, interval=interval, group_by='ticker')
    return data
