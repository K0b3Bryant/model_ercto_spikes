import requests

def lme_importer(metal_code):
    """ Pull LME official prices and inventory levels (requires subscription for full API). """
    url = f'https://www.lme.com/api/Official/{metal_code}'  # hypothetical endpoint
    df = pd.DataFrame(requests.get(url).json())
    df['Date'] = pd.to_datetime(df['date'])
    df.set_index('Date', inplace=True)
    return df
