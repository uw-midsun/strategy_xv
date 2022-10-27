import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import pandas as pd
from weather_forecast.get_weather import *
from weather_forecast.config import API_KEY


"""
- Test weather forecast functions from /weather_forecast/get_weather.py
- Retrieving along a route is not tested, however, it is in practice the same as retrieving individual forecasts from each point
- The API key is retrieved from config.py, refer to the README inside weather_forecast for specifics
"""

def test_api_call():
    waterloo_lat, waterloo_lon = -79.411209, 43.759838
    weather_data = get_weather_1h(waterloo_lat, waterloo_lon)
    assert(isinstance(weather_data, list) and len(weather_data) > 0)

# Test if an illegal precision value is used
def test_precision_negative():
    waterloo_lat, waterloo_lon = -79.411209, 43.759838
    weather_data = get_weather(waterloo_lat, waterloo_lon, "2m")
    assert(len(weather_data) == 0)

# Test when the requested forecast interval is larger than supported, the function uses the maximum available interval
def test_forecast_interval_negative():
    waterloo_lat, waterloo_lon = 43.759838, -79.411209
    weather_data = get_weather(waterloo_lat, waterloo_lon, "30m", "7h")
    assert(len(weather_data) == 13)  #Weather data should return thirteen 30m intervals for 6 hours, as +6h to +6.5h included