def cot_importer(futures_code):
    """ Download COT report data (weekly) from CFTC. """
    url = f'https://www.cftc.gov/files/dea/history/fut_fin_xls/{futures_code}_fut.xls'
    df = pd.read_excel(url, sheet_name=0, skiprows=0)
    df['Date'] = pd.to_datetime(df['Report_Date_as_MM_DD_YYYY'])
    df.set_index('Date', inplace=True)
    return df
