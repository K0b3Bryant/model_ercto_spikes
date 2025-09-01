def ercot_importer(url):
    """ Import ERCOT LMP (Locational Marginal Price) CSV file. """
    df = pd.read_csv(url)
    
    # Example standardization
    df['Datetime'] = pd.to_datetime(df['HE'] + ' ' + df['Date'], format='%H %m/%d/%Y')
    df.set_index('Datetime', inplace=True)
    
    # Optional: pivot to have locations as columns
    df = df.pivot(index='Datetime', columns='Node', values='LMP')
    
    return df
