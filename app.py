from flask import Flask
from flask import render_template , request
from weather import get_coordinates , get_weather
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')

GEO_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home() :
    if request.method == 'POST' :
        city = request.form.get('city')

        coordinates = get_coordinates(city=city)
        if coordinates[0] is None:
            return  render_template('index.html',error="City not found. Try another one.")
    
        elif coordinates[0] == 'Connection_Error' :
            return render_template('index.html',error="Network error. Try again later.")
    
        elif isinstance(coordinates[0],int) :
            return render_template('index.html',error=f"API error: {coordinates[0]}")

        else :
            lat,lon = coordinates
            weather = get_weather(lat,lon,'en')
            return render_template('index.html' , weather=weather)
           
    return render_template('index.html')
if __name__ == '__main__' :
    app.run(debug=True)