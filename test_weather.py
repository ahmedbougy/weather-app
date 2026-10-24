from weather import display_weather , get_coordinates , get_weather , CityNotFoundError , APIConnectionError
from unittest.mock import patch
import pytest
import requests
# get weather function Teste
@patch('weather.requests.get')
def test_get_weather_success(mok_get) :
    mok_response = mok_get.return_value
    mok_response.ok = True
    mok_response.json.return_value = {
    'weather': [{'description': 'clear sky'}],
    'main': {
        'temp': 20.0,
        'feels_like': 19.0,
        'temp_min': 18.0,
        'temp_max': 22.0,
        'pressure': 1015,
        'humidity': 50,
        # sea_level, grnd_level اختيارية (يستخدم get)
    },
    'visibility': 10000,
    'wind': {'speed': 5.0, 'deg': 180},
    'clouds': {'all': 10},
    'sys': {'country': 'DZ'},
    'timezone': 3600,
    'name': 'Constantine',
    }
    
    result = get_weather(36.36, 6.60, 'en')
    assert result['temp'] == 20.0
    assert result['description'] == 'clear sky'
    assert result['name'] == 'Constantine'
    assert isinstance(result, dict)

@patch('weather.requests.get')
def test_get_weather_APIConnectionError(mock_get) :
    mock_response = mock_get.return_value
    mock_response.ok = False
    with pytest.raises(APIConnectionError) :
        get_weather(36.36, 6.60, 'en')

@patch('weather.requests.get')
def test_get_weather_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout('Request timed out')
    with pytest.raises(APIConnectionError):
        get_weather(36.36, 6.60, 'en')

@patch('weather.requests.get')
def test_get_weather_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError('No internet connection')
    with pytest.raises(APIConnectionError):
        get_weather(36.36, 6.60, 'en')

#get coordinates function Test
@patch('weather.requests.get')
def test_get_coordinates_success(mok_get) :
    mok_response = mok_get.return_value
    mok_response.ok = True
    mok_response.json.return_value = [
        {'lat': 36.36, 'lon': 6.60, 'name': 'Constantine'}
    ]

    lat , lon = get_coordinates('Constantine,DZ')

    assert lat == 36.36
    assert lon == 6.60

@patch('weather.requests.get')
def test_get_coordinates_city_not_found(mock_get) :
    mock_response = mock_get.return_value
    mock_response.ok = True
    mock_response.json.return_value = []   # ← قائمة فارغة
    
    with pytest.raises(CityNotFoundError):
        get_coordinates('xyzabc123')

@patch('weather.requests.get')
def test_get_coordinates_APIConnectionError(mock_get) : 
    mock_response = mock_get.return_value
    mock_response.ok = False
    with pytest.raises(APIConnectionError) :
        get_coordinates('Constantine.DZ')

@patch('weather.requests.get')
def test_get_coordinates_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout('Request timed out')
    with pytest.raises(APIConnectionError):
        get_coordinates('Constantine,DZ')

@patch('weather.requests.get')
def test_get_coordinates_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError('No internet connection')
    with pytest.raises(APIConnectionError):
        get_coordinates('Constantine,DZ')

#display weather Test
def test_display_weather_english() :
    fake_data = {
        'name': 'Constantine',
        'country': 'DZ',
        'temp': 20.0,
        'feels_like': 19.0,
        'temp_min': 18.0,
        'temp_max': 22.0,
        'humidity': 50,
        'pressure': 1015,
        'visibility': 10000,
        'wind_speed': 5.0,
        'wind_deg': 180,
        'clouds': 10,
        'description': 'clear sky',
    }

    result = display_weather(fake_data, lang='en')

    assert 'Constantine'  in result
    assert '20.0' in result
    assert 'clear sky' in result
    assert isinstance(result, str)

def test_display_weather_arabic():
    fake_data = {
        'name': 'قسنطينة',
        'country': 'DZ',
        'temp': 20.0,
        'feels_like': 19.0,
        'temp_min': 18.0,
        'temp_max': 22.0,
        'humidity': 50,
        'pressure': 1015,
        'visibility': 10000,
        'wind_speed': 5.0,
        'wind_deg': 180,
        'clouds': 10,
        'description': 'سماء صافية',
    }

    result = display_weather(fake_data,lang='ar')
    assert 'قسنطينة' in result
    assert '20.0' in result
    assert 'سماء صافية' in result
    assert isinstance(result, str)

def test_display_weather_none():
    result = display_weather(None)
    assert result == 'No data available.'
    assert isinstance(result, str)

