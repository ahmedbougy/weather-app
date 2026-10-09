from flask import Flask
from flask import render_template , request
from weather import (
    get_coordinates,
    get_weather,
    WeatherAppError,
    APIConnectionError,
    CityNotFoundError
    )

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home() :
    if request.method == 'POST' :
        city = request.form.get('city')
        try :
            lat,lon = get_coordinates(city=city)
            weather = get_weather(lat,lon,'en')
            return render_template('index.html', weather=weather)
        except APIConnectionError as e:
            return render_template('index.html', error=str(e))
        except CityNotFoundError as e :
            return render_template('index.html', error=str(e))
        except WeatherAppError as e :
            return render_template('index.html', error=str(e))
        except Exception as e :
            return render_template('index.html', error=f'Unexpected error: {e}')
        
        
           
    return render_template('index.html')
if __name__ == '__main__' :
    app.run(debug=True)