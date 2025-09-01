import requests
import pandas as pd
from datetime import datetime

def weather_importer(city, api_key, start=None, end=None):
    """ Fetch historical weather data from OpenWeatherMap for a given city. """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    records = []
    for item in data['list']:
        dt = datetime.fromtimestamp(item['dt'])
        temp = item['main']['temp']
        humidity = item['main']['humidity']
        wind_speed = item['wind']['speed']
        records.append({'date': dt, 'temp': temp, 'humidity': humidity, 'wind_speed': wind_speed})
    
    df = pd.DataFrame(records)
    
    # Filter by start/end if provided
    if start:
        df = df[df['date'] >= pd.to_datetime(start)]
    if end:
        df = df[df['date'] <= pd.to_datetime(end)]
    
    return df
