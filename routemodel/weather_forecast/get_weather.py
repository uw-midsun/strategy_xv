import requests
import pandas as pd
import datetime
import dateutil
import json

import os
from dotenv import load_dotenv

load_dotenv()


FORECAST_URL_BASE = "https://api.tomorrow.io/v4/timelines"
API_KEY = os.environ.get("TOMORROW_IO_API_KEY")


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

class Weather:
    def __init__(self, units = "metric", requested_fields=[]):
        # Headers for API Call
        self.headers  = {
            "accept": "application/json",
            "Accept-Encoding": "gzip"
        }

        # Information fields to request from the API
        if len(requested_fields) <= 0:
            self.requested_fields = [
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
        else:
            self.requested_fields = requested_fields

         # Specifies the maximum forecast that can be requested, as described by the API documentation
        self.timestep_forecast_range_dict = {
            "1m": "6h",
            "5m": "6h",
            "15m": "6h",
            "30m": "6h",
            "1h": "360h",
            "1d": "15d",
        }

        # Loads Tomorrow.io weather codes
        self.weather_codes = json.load(open(os.path.join(os.path.dirname(__file__), "weather_codes.json")))
        # Measurement system returned by API calls
        units = units.lower()
        if units == "metric" or units == "imperial":
            self.units = units
        else:
            units = "metric"

    def set_requested_fields(self, requested_fields):
        self.requested_fields = requested_fields

    def get_requested_fields(self):
        return self.requested_fields

    def set_units(self, units):
        units = units.lower()
        if units == "metric" or units == "imperial":
            self.units = units
        else:
            units = "metric"

    def get_units(self):
        return self.units

    def validated_forecast_interval(self, timestep, forecast_range):
        """
        Based on the given timestep, determines if the forecast range is valid
        If invalid, the function returns an adjusted forecast range
        @param timestep: string containing the timestep of each forecast
        @param forecast_range: string contianing the range of the total forecast
        @return: a formatted string that can be used in the API call
        """
        end_time = ""

        if forecast_range:
            if timestep_to_minute(forecast_range) <= timestep_to_minute(self.timestep_forecast_range_dict[timestep]):
                end_time = "nowPlus{}".format(forecast_range)
            else:
                print("(get_weather.py) The requested forecast interval is larger than the interval supported by the API\n \
                Forecast for {} returned instead".format(self.timestep_forecast_range_dict[timestep]))
                end_time = "nowPlus{}".format(self.timestep_forecast_range_dict[timestep])
        else:
            end_time = "nowPlus{}".format(self.timestep_forecast_range_dict[timestep])

        return end_time

    def process_weather_timelines_json(self, lat, lon, timestep, timelines_json):
        """
        Takes the JSON returned by the API and retyrbs data as a list of dicts
        @param lat: string containing latitude value
        @param lon: string containing longitude value
        @param timestep: string containing the timestep of each forecast
        @param timelines_json: Weather API JSON
        @return: list of lists, each inner list contains entries for one timestep in the format [start_time, end_time, weather_dict]
        """

        weather_data = timelines_json["data"]["timelines"][0]
        weather_forecast = []

        for weather in weather_data["intervals"]:
            weather_dict = {
                'latitude': lat,
                'longitude': lon,
            }
            
            values = weather["values"]
            for field in self.requested_fields:
                if field == "weatherCode":
                    weather_dict["weatherDescription"] = self.weather_codes.get(str(values.get("weatherCode", "NA")), None)
                else:
                    weather_dict[field] = values.get(field, None)

            weather_start_time = (dateutil.parser.isoparse(weather["startTime"])).isoformat()
            weather_end_time = (dateutil.parser.isoparse(weather["startTime"]) + 
                                datetime.timedelta(minutes=timestep_to_minute(timestep))).isoformat()
            weather_forecast.append([weather_start_time, weather_end_time, weather_dict])

        return weather_forecast

    def get_weather(self, lat, lon, timestep, forecast_range=""):
        """
        Calls Tomorrow.io API to get weather data and returns data as a list of dicts
        @param lat: string containing latitude value
        @param lon: string containing longitude value
        @param timestep: string containing the timestep of each forecast
        @param forecast_range: string containing the range of the total forecast
        @return: list of lists, each inner list contains entries for one timestep in the format [start_time, end_time, weather_dict]
        """
        start_time = "now"

        # Validates that the timestep amount is supported by the API
        if timestep not in self.timestep_forecast_range_dict.keys():
            print("(get_weather.py) Unsupported forecast timestep")
            return []

        # Attempts to set the end time using the maximum interval allowed
        end_time = self.validated_forecast_interval(timestep, forecast_range)
            
        # Building the URL
        url = FORECAST_URL_BASE + "?"
        url += "location={}%2C%20{}".format(lat, lon)
        for field in self.requested_fields:
            url += "&fields={}".format(field)
        url += "&units={}".format(self.units)
        url += "&timesteps={}".format(timestep)
        url += "&startTime={}&endTime={}".format(start_time, end_time)
        url += "&apikey={}".format(API_KEY)

        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            forecast = self.process_weather_timelines_json(lat, lon, timestep, response.json())
            return forecast
        return []

    def get_weather_1h(self, lat, lon):
        return self.get_weather(lat, lon, "15m", "1h")

    def get_weather_6h(self, lat, lon):
        return self.get_weather(lat, lon, "15m", "6h")

    def get_weather_1d(self, lat, lon):
        return self.get_weather(lat, lon, "1h", "1d")

    def get_weather_7d(self, lat, lon):
        return self.get_weather(lat, lon, "1d", "7d")

    def get_weather_14d(self, lat, lon):
        return self.get_weather(lat, lon, "1d", "14d")
