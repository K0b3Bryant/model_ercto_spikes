import wbdata
import datetime

def worldbank_import(indicators, countries='all', start=None, end=None):
    """ Fetch World Bank data. """
    
    if start is None: start = datetime.datetime(2000, 1, 1)
    if end is None: end = datetime.datetime.today()
        
    return wbdata.get_dataframe(indicators, country=countries, data_date=(start, end))
