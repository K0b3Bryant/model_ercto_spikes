def imf_importer(dataset_code):
    """ IMF Primary Commodity Prices dataset. """
    url = f'https://www.imf.org/external/datamapper/api/{dataset_code}.csv'
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['DATE'])
    df.set_index('Date', inplace=True)
    return df
