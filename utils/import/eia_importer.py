import requests

def eia_import(series_id, api_key):
    """ Fetch EIA series data (e.g., petroleum, natural gas) """
    url = f"http://api.eia.gov/series/?series_id={series_id}&api_key={api_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['series'][0]['data'], columns=['Date', series_id])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df[series_id] = df[series_id].astype(float)
    return df
