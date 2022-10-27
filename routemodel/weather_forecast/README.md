# **Using get_weather.py**

The goal of get_weather.py is to hit the API and collect information on the weather for different forecast intervals. Currently, the API supports up to 14-day forecasting.

In order for the function to work, you must get an API key from [Tomorrow.io](https://www.tomorrow.io/weather-api/). 

Then, create a `config.py` file in the same directory as `get_weather.py` and store your API Key as a string.

```
API_KEY = '<KEY>'
``` 
&nbsp;

# **Main Function**

The first function provided below is the main parent function. Beneath it are some helper functions set with default values for ease of use. 
<br><br/>


## get_weather(lat, lon, precision, forecast_interval="")

The `get_weather` function takes in three mandatory parameters and one optional parameter. The function returns a list of lists. Each inner list contains three elements corresponding to one timestep, `[start_time, end_time, weather_data]`. The variable `weather_data` is a dictionary with the reqested data fields. The data fields are automatically set in the function and are not currently customizable.

* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float
* `timestep` - accepts one of the following string values `"1m"`, `"5m"`, `"15m"`, `"30m"`, `"1h"` or `"1d"` to determine the intervals at which weather data is returned
* `forecast_range` - an optional parameter that accepts strings of the form `"{number}{time_unit}"` (e.g `"4d"`, `"45m"`, etc.), the maximum range is given by the [Tomorrow.io Documentation](https://docs.tomorrow.io/reference/data-layers-overview)

If the given `timestep` is invalid, a message will be printed to the console and an empty list is returned.
If the given `forecast_range` is invalid, it will be replaced with the maximum range provided by the API.

### **Return Values**
The dictionary returned by the function contains the following entries:
* Latitude - `float`
* Longitude - `float`
* Temperature (C) - `float`
* Wind Speed (m/s) - `float`
* Wind Direction - `int`
* Weather - `string`
* Pressure (hPa) - `float`
* Precipitation (mm/hr) - `int`
* Cloud Cover (%) - `int`
* Humidity (%) - `int`

Any values that are not available from the weather API will be returned as `None`. 
<br><br/>


# **Helper Functions**

The following helper functions accept two parameters:
* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float

## **get_weather_1h(lat, lon)**

Calls the `get_weather` parent function with a `"15m"` timestep and a `"1h"` forecast range.

## **get_weather_6h(lat, lon)**

Calls the `get_weather` parent function with a `"15m"` timestep and a `"6h"` forecast range.

## **get_weather_1d(lat, lon)**

Calls the `get_weather` parent function with a `"1h"` timestep and a `"1d"` forecast range.

## **get_weather_7d(lat, lon)**

Calls the `get_weather` parent function with a `"1d"` timestep and a `"1d"` forecast range.

## **get_weather_14d(lat, lon)**

Calls the `get_weather` parent function with a `"1d"` timestep and a `"14d"` forecast range.
