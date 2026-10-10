import requests
from dotenv import load_dotenv
import os
import logging 
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(BASE_DIR,'app.log'),
    filemode='a'

)
load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')

GEO_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

class WeatherAppError(Exception) :
    """Base class for all weather app errors."""
    pass

class CityNotFoundError(WeatherAppError):
    pass

class APIConnectionError(WeatherAppError):
    pass


def get_coordinates(city: str) -> tuple[float, float]:
    """
    Get latitude and longitude for a city name.

    Args:
        city(str): City name(e.g, "Constantine,DZ")

    Returns:
        tuple: (latitude, longitude) 

    Raises:
        CityNotFoundError: if city not found
        APIConnectionError: if network or API fails
    """

    params = {
        'q':city,
        'appid':api_key ,
        'limit': 1,
    }
    try :
        response = requests.get(url=GEO_URL , params=params,timeout=10)
    except requests.exceptions.ConnectionError :
        logging.error('No internet connection')
        raise APIConnectionError('No internet connection')
    except requests.exceptions.Timeout :
        logging.error('Request timed out')
        raise APIConnectionError('Request timed out')

    if not response.ok :
        logging.error(f'API error: {response.status_code}')
        raise APIConnectionError(f'API error: {response.status_code}')

    data = response.json()
    if not data :
        logging.error(f'City not found: {city}')
        raise CityNotFoundError(f'City not found: {city}')

    return data[0]['lat'], data[0]['lon']

def get_weather(lat: float, lon: float, lang: str ='en') -> dict :
    """
    Get weather data for coordinates.

    Args:
        lat(float): Latitude.
        lon(float): Longitude.
        lang(str): Language code ('en' or 'ar'). Default to 'en'.
        
    Returns:
        dict: Weather information.

    Raises:
        APIConnectionError: if network or API fails.

    """
    if lang not in ('en' , 'ar') :
        lang = 'en'
    params = {
        'lat':lat,
        'lon':lon,
        'appid':api_key,
        'lang':lang,
        'units':'metric'
    }

    try :
        response = requests.get(url=WEATHER_URL , params=params , timeout=10)
    except requests.exceptions.ConnectionError :
        logging.error('No internet connection')
        raise APIConnectionError('No internet connection')
    except requests.exceptions.Timeout :
        logging.error('Request timed out')
        raise APIConnectionError('Request timed out')

    if not response.ok :
        logging.error(f'API error: {response.status_code}')
        raise APIConnectionError(f'API error: {response.status_code}')
           
    data = response.json()
    
    description_list = data['weather']
    description = description_list[0]['description']
    
    main_data = data['main']
    temp = main_data['temp']
    feels_like = main_data['feels_like']
    temp_min = main_data['temp_min']
    temp_max = main_data['temp_max']
    pressure = main_data['pressure']
    humidity = main_data['humidity']
    sea_level = main_data.get('sea_level','N/A')
    grnd_level = main_data.get('grnd_level','N/A')

    visibility = data['visibility']
    wind = data['wind']
    wind_speed = wind['speed']
    wind_deg = wind['deg']
    wind_gust = wind.get('gust')

    clouds = data['clouds']['all']

    sys = data['sys']
    country = sys['country']

    timezone = data['timezone']
    name = data['name']

    weather_info = {
        "description": description,
        "temp": temp,
        "feels_like": feels_like,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "pressure": pressure,
        "humidity": humidity,
        "sea_level": sea_level,
        "grnd_level": grnd_level,
        "visibility": visibility,
        "wind_speed": wind_speed,
        "wind_deg": wind_deg,
        "wind_gust": wind_gust,
        "clouds": clouds,
        "country": country,
        "timezone": timezone,
        "name": name
    }

    return weather_info
        

def display_weather(weather_info: dict, lang: str ='en') -> str:
    """
    Format weather data for display.

    Args:
        weather_info(dict): Weather data from get_weather.
        lang(str): Language code ('en' or 'ar'). Defaults to 'en'

    Returns:
        str: Formatted weather report.

    """
    if lang not in ('en' , 'ar') :
        lang = 'en'

    if weather_info is None:
        return "No data available."

    if lang == 'ar':
        return f'''
🌤️  الطقس في {weather_info['name']}، {weather_info['country']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  الحرارة: {weather_info['temp']}°C (تُحس كأنها {weather_info['feels_like']}°C)
📊  الصغرى: {weather_info['temp_min']}°C | الكبرى: {weather_info['temp_max']}°C
💧  الرطوبة: {weather_info['humidity']}%
🌬️  الضغط: {weather_info['pressure']} hPa
👁️  الرؤية: {weather_info['visibility']} م
💨  الرياح: {weather_info['wind_speed']} م/ث باتجاه {weather_info['wind_deg']}°
☁️  الغيوم: {weather_info['clouds']}%
📝  الحالة: {weather_info['description']}
'''
    else :
        return f'''
🌤️  Weather in {weather_info['name']}, {weather_info['country']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature: {weather_info['temp']}°C (feels like {weather_info['feels_like']}°C)
📊  Min: {weather_info['temp_min']}°C | Max: {weather_info['temp_max']}°C
💧  Humidity: {weather_info['humidity']}%
🌬️  Pressure: {weather_info['pressure']} hPa
👁️  Visibility: {weather_info['visibility']} m
💨  Wind: {weather_info['wind_speed']} m/s at {weather_info['wind_deg']}°
☁️  Clouds: {weather_info['clouds']}%
📝  Condition: {weather_info['description']}
    '''

def main() -> None :
    lang = input("Language (ar/en): ").strip() or 'en'
    city = input('Enter the name of the city :\n')
    try :
        lat , lon =  get_coordinates(city=city)
        weather = get_weather(lat=lat, lon=lon, lang=lang)
        print(display_weather(weather, lang))

    except APIConnectionError as e :
        print(e)
    except CityNotFoundError as e :
        print(e)
    except WeatherAppError as e:
        print(f"Unexpected error: {e}")
    except Exception as e:               # ← (اختياري) أي شيء آخر
        print(e)

if __name__ == '__main__' :
    main()
