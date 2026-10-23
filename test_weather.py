from weather import display_weather

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
