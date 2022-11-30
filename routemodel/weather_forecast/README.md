# **Using get_weather.py**

The goal of get_weather.py is to hit the API and collect information on the weather for different forecast intervals. Currently, the API supports up to 14-day forecasting.

The functions are implemented in the Weather class. In order for the functions to work, you must get an API key from [Tomorrow.io](https://www.tomorrow.io/weather-api/). 

The code uses environment variables through `python-dotenv`. To run the code, create a `.env` file and store your API Key as `TOMORROW_IO_API_KEY`.

```
TOMORROW_IO_API_KEY = <KEY>
``` 

To start using the class, we'll have to initialize an instance of the Weather class inside the python file we are working with.
<br><br/>

# **Initializing the Weather Class**

The class constructor is defined as follows

`def __init__(self, units = "metric", requested_fields=[])`

The class accepts two optional parameters, `units` and `fields`. The variable `units` can either be set to `"metric"` or `"imperial"`, but by default it will be set to `"metric"`. The `fields` parameter must be a list of strings taken from valid [API data fields](https://docs.tomorrow.io/reference/data-layers-core). By default, the `fields` variable will be filled out with a pre-set list of fields. The chosen defaults can be found in the return values of the `get_weather` function (see below).

Outside of the initialization, the fields can also be set using

`def set_requested_fields(self, requested_fields)`

The `fields` parameter is the same as described in the constructor.
<br><br/>

Example code for initializing the Weather class is shown below:

```
from weather_forecast.get_weather import Weather

forecast_api = Weather()

new_fields = ["temperature", "humidity", "windSpeed"]
forecast_api.set_requested_fields(new_fields)
```

Next, we'll cover the major functions in the Weather class.
<br><br/>

# **Main Function**

The first function provided below is the main function in the class. Beneath it are some helper functions set with default values for ease of use. 
<br><br/>

## Weather.get_weather(lat, lon, precision, forecast_interval="")

The `get_weather` function takes in three mandatory parameters and one optional parameter. The function returns a list of lists. Each inner list contains three elements corresponding to one timestep, `[start_time, end_time, weather_data]`. The variable `weather_data` is a dictionary with the reqested data fields.

* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float
* `timestep` - accepts one of the following string values `"1m"`, `"5m"`, `"15m"`, `"30m"`, `"1h"` or `"1d"` to determine the intervals at which weather data is returned
* `forecast_range` - an optional parameter that accepts strings of the form `"{number}{time_unit}"` (e.g `"4d"`, `"45m"`, etc.), the maximum range is given by the [Tomorrow.io Documentation](https://docs.tomorrow.io/reference/data-layers-overview)

If the given `timestep` is invalid, a message will be printed to the console and an empty list is returned.
If the given `forecast_range` is invalid, it will be replaced with the maximum range provided by the API.

### **Return Values**
By default, if the default `requested_fields` has not been changed, the dictionary returned by the function contains the following entries:
* latitude - `float`
* longitude - `float`
* temperature - `float`
* windSpeed - `float`
* windDirection - `int`
* weather - `string`
* pressure - `float`
* precipitation - `int`
* cloudCover - `int`
* humidity - `int`

The actual units represented by the variables can be found in the [Tomorrow.io documentation](https://docs.tomorrow.io/reference/data-layers-overview).

Any values that are not available from the weather API will be returned as `None`. 
<br><br/>


# **Helper Functions**

The following helper functions accept two parameters:
* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float

## Weather.get_weather_1h(lat, lon)

Calls the `get_weather` parent function with a `"15m"` timestep and a `"1h"` forecast range.

## Weather.get_weather_6h(lat, lon)

Calls the `get_weather` parent function with a `"15m"` timestep and a `"6h"` forecast range.

## Weather.get_weather_1d(lat, lon)

Calls the `get_weather` parent function with a `"1h"` timestep and a `"1d"` forecast range.

## Weather.get_weather_7d(lat, lon)

Calls the `get_weather` parent function with a `"1d"` timestep and a `"1d"` forecast range.

## Weather.get_weather_14d(lat, lon)

Calls the `get_weather` parent function with a `"1d"` timestep and a `"14d"` forecast range.
