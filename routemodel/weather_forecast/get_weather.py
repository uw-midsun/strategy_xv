import requests
import pandas as pd
import datetime
import dateutil
import json

import os.path
from .config import API_KEY


FORECAST_URL_BASE = "https://api.tomorrow.io/v4/timelines"


def timestep_to_minute(timestep):
    """
    Converts a given timestep string into a standard integer in minutes
    @param timestep: string in the format of a number followed by 'm','h' or 'd'
    """
    timestep_minute_vals = {
        "m": 1,
        "h": 60,
        "d": 1440,
    }

    try:
        minutes = int(timestep[:-1]) * timestep_minute_vals[timestep[-1]]
        return minutes
    except:
        print("(get_weather.py) Timestep was given in an inappropriate format, timestep_to_minute will return 0")
        return 0


def get_weather(lat, lon, timestep, forecast_range=""):
    """
    Calls Tomorrow.io API to get weather data and returns data as a list of dicts
    @param lat: string containing latitude value
    @param lon: string containing longitude value
    @param timestep: string containing the timestep of each forecast
    @param forecast_range: string containing the range of the total forecast
    @return: list of lists, each inner list contains entries for one timestep in the format [start_time, end_time, weather_dict]
    """

    # Headers for API Call
    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip"
    }

    # Information fields to request from the API
    requested_fields = [
        "temperature",
        "windSpeed",
        "windGust",
        "windDirection",
        "weatherCode",
        "pressureSurfaceLevel",
        "precipitationIntensity",
        "precipitationType",
        "humidity",
        "cloudCover",
    ]

    # Specifies the maximum forecast that can be requested, as described by the API documentation
    timestep_forecast_range_dict = {
        "1m": "6h",
        "5m": "6h",
        "15m": "6h",
        "30m": "6h",
        "1h": "360h",
        "1d": "15d",
    }

    weather_codes = json.load(open(os.path.join(os.path.dirname(__file__), "weather_codes.json")))

    units = "metric"
    start_time = "now"

    # Validates that the timestep amount is supported by the API
    if timestep not in timestep_forecast_range_dict.keys():
        print("(get_weather.py) Unsupported forecast timestep")
        return []

    # Attempts to set the end time using the maximum interval allowed
    if forecast_range:
        if timestep_to_minute(forecast_range) <= timestep_to_minute(timestep_forecast_range_dict[timestep]):
            end_time = "nowPlus{}".format(forecast_range)
        else:
            print("(get_weather.py) The requested forecast interval is larger than the interval supported by the API\n \
            Forecast for {} returned instead".format(timestep_forecast_range_dict[timestep]))
            end_time = "nowPlus{}".format(timestep_forecast_range_dict[timestep])
    else:
        end_time = "nowPlus{}".format(timestep_forecast_range_dict[timestep])

    # Building the URL
    url = FORECAST_URL_BASE + "?"
    url += "location={}%2C%20{}".format(lat, lon)
    for field in requested_fields:
        url += "&fields={}".format(field)
    url += "&units={}".format(units)
    url += "&timesteps={}".format(timestep)
    url += "&startTime={}&endTime={}".format(start_time, end_time)
    url += "&apikey={}".format(API_KEY)

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        weather_data = response.json()["data"]["timelines"][0]
        weather_forecast = []

        for weather in weather_data["intervals"]:
            weather_dict = {
                'Latitude': lat,
                'Longitude': lon,
                'Temperature (C)': weather["values"].get("temperature", None),
                'Wind Speed (m/s)': weather["values"].get("windSpeed", None),
                'Wind Direction': weather["values"].get("windDirection", None),
                'Weather': weather_codes.get(str(weather["values"].get("weatherCode", "NA")), None),
                'Pressure (hPa)': weather["values"].get("pressureSurfaceLevel", None),
                'Precipitation (mm/hr)': weather["values"].get("precipitationIntensity", None),
                'Cloud Cover (%)': weather["values"].get("cloudCover", None),
                'Humidity (%)': weather["values"].get("humidity", None),
            }

            weather_start_time = (dateutil.parser.isoparse(weather["startTime"])).isoformat()
            weather_end_time = (dateutil.parser.isoparse(weather["startTime"]) + 
                                datetime.timedelta(minutes=timestep_to_minute(timestep))).isoformat()
            weather_forecast.append([weather_start_time, weather_end_time, weather_dict])

        return weather_forecast
    return []

def get_weather_1h(lat, lon):
    return get_weather(lat, lon, "15m", "1h")

def get_weather_6h(lat, lon):
    return get_weather(lat, lon, "15m", "6h")

def get_weather_1d(lat, lon):
    return get_weather(lat, lon, "1h", "1d")

def get_weather_7d(lat, lon):
    return get_weather(lat, lon, "1d", "7d")

def get_weather_14d(lat, lon):
    return get_weather(lat, lon, "1d", "14d")
