import requests

def noaa_importer(city, api_key):
    """ Fetch current weather forecast data for a city. """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    records = [{'date': pd.to_datetime(item['dt'], unit='s'),
                'temp': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed']} 
               for item in data['list']]
    return pd.DataFrame(records).set_index('date')
