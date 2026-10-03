import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')

GEO_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_coordinates(city) :
    params = {
        'q':city,
        'appid':api_key ,
        'limit': 1,
    }
    try :
        response = requests.get(url=GEO_URL , params=params)

        if not response.ok:
            return response.status_code, None
            
        data = response.json()

        if not data :
            
            return None,None
        else :
            lat = data[0]['lat']
            lon = data[0]['lon']

            return lat,lon
    except requests.exceptions.ConnectionError:
       
        return 'Connection_Error',None
    
def get_weather(lat,lon,lang) :
    if lang != 'ar' and lang != 'en' :
        lang = 'en'
    params = {
        'lat':lat,
        'lon':lon,
        'appid':api_key,
        'lang':lang,
        'units':'metric'
    }
    try :
        response = requests.get(url=WEATHER_URL , params=params)

        status_code = response.status_code 
        
        if response.ok :
            response = response.json()
            
            description_list = response['weather']
            description = description_list[0]['description']
            
            main_data = response['main']
            temp = main_data['temp']
            feels_like = main_data['feels_like']
            temp_min = main_data['temp_min']
            temp_max = main_data['temp_max']
            pressure = main_data['pressure']
            humidity = main_data['humidity']
            sea_level = main_data.get('sea_level','N/A')
            grnd_level = main_data.get('grnd_level','N/A')

            visibility = response['visibility']
            wind = response['wind']
            wind_speed = wind['speed']
            wind_deg = wind['deg']
            wind_gust = wind.get('gust')

            clouds = response['clouds']['all']

            sys = response['sys']
            country = sys['country']

            timezone = response['timezone']
            name = response['name']

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
        else :
            print(f"Wrong : {status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None

def display_weather(weather_info,lang):
    if lang != 'ar' and lang != 'en' :
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

def main() :
    lang = input("Language (ar/en): ").strip() or 'en'
    city = input('Enter the name of the city :\n')
    coordinates = get_coordinates(city=city)
    
    if coordinates[0] is None:
        print("There is no city by that name; try another one.")

    elif coordinates[0] == 'Connection_Error' :
         print("No internet connection")

    elif isinstance(coordinates[0],int) :
        print(f"API error: {coordinates[0]}")

    else:
        lat,lon = coordinates
        weather_dic = get_weather(lat,lon,lang)
        weather_str = display_weather(weather_info=weather_dic,lang=lang)
        print(weather_str)

if __name__ == '__main__' :
    main()
