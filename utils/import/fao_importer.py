def fao_importer(indicator_code):
    """ Fetch FAO data via their API or CSV download. """
    url = f'http://www.fao.org/faostat/en/#data/QC/{indicator_code}'  # CSV endpoint varies
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Year'], format='%Y')
    df.set_index('Date', inplace=True)
    return df
