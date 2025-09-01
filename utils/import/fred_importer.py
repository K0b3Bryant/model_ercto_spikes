from fredapi import Fred
import pandas as pd

def fetch_fred_series(tickers, api_key, start=None, end=None):
    """ Fetch multiple series from FRED and return a merged DataFrame. """
    fred = Fred(api_key=api_key)
    df_list = []

    for ticker in tickers:
        series = fred.get_series(ticker, observation_start=start, observation_end=end)
        df = pd.DataFrame(series, columns=[ticker])
        df.index.name = 'Date'
        df_list.append(df)

    # Merge all series on date
    merged_df = pd.concat(df_list, axis=1)
    return merged_df
