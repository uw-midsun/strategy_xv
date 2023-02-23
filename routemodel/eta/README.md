# **ETA Class**

The ETA class provides functions to retrieve an estimated time of arrival for the vehicle at specific checkpoints along the race route.
Checkpoints as they pertain to `eta.py` are defined as points that are 1000m apart along the race route. Although, the distance can be adjusted as needed.

The main motivation behing the ETA class is to provide information to support the weather API. The ETA class allows us to reduce the number of API calls and only grab weather forecasts that will likely be relevant as we do not want to constantly be making API calls for every point along the race route. 


To start using the class, we'll have to initialize an instance of the ETA class inside the python file we are working with.
<br><br/>

# **Initializing the ETA Class**

The class constructor is defined as follows

`def __init__(self, route, lat=0, lon=0):`

The class accepts the `route` parameter and two optional `lat` and `lon` parameters. 

The `lat` and `lon` parameters initialize the car's initial position, however, most methods update the location by default, so these parameters should not be necessary in most use cases.

`route` is a collection of lat/lon points used to generate the checkpoints as well as the more precise race route. To generate the more precise race route, `eta.py` currently uses a code snippet from the overhaul branch, however, it can be properly integrated in future iterations.

Example code for initializing the ETA class is shown below:

```
from eta.eta import ETA

# A set of random coordinates along a highway
coords = [
        [43.435784827874585, -80.45663435546756],
        [43.44214170089898, -80.45680601683284],
        [43.45684719975201, -80.47105391015053],
        [43.46220509439163, -80.47139723288107],
        [43.47640744733148, -80.42985518248491],
        [43.48138993815619, -80.4190405164727],
        [43.4921009021235, -80.41200240049649],
        [43.51003128688014, -80.35707076360902],
    ]

eta = ETA(coords)
```

# **Inside the ETA Object**
There are a couple key variables inside an instance of the ETA object and understanding their structure will help with the overall understanding of the methods as well.

## `route_model`

All classes inside the Strategy repository should have access to reading and writing from the `route_model` dataframe/database. The component most significant to `eta.py` is that the `route_model` dataframe contains precise coordinates modelling the race route. Many methods in the ETA class will make use of this to perform more accurate calculations.

## `checkpoint_coords`

Checkpoints will typically be referred to by an index, i.e. 'Checkpoint 0', 'Checkpoint 3'. The `checkpoint_coords` variable contains a list of lat/lon pairs. Each of the lat/lon pairs represent the location of a checkpoint and are placed at intervals of 1000m. 


The first checkpoint always corresponds to the first coordinates in the `route_model` dataframe. Notably, each checkpoint directly corresponds to one of the `route_model` points. Additionally, the `route_model` dataframe contains a column called `checkpoint` which describes the last checkpoint the car would have crossed by that point.

## `eta`

A list of `float` values representing the time (in minutes) it will take for the car to travel to a given checkpoint. The values in `eta` each correspond to a specific checkpoint, i.e. `eta[0]` is the time it will take to reach `checkpoint_coords[0]`. If the value is `-1` then the checkpoint has already been passed.

Next, we'll cover the major functions in the ETA class.
<br><br/>

# **Main Function**

The function provided below is the main function in the class. 

## `get_eta()`

The `get_eta` method does not require any parameters. It uses information such as the race route and checkpoints which are generated when the ETA object is initialized. 

### **Return Value**
The `get_eta` method returns a list of `float` values representing the time it takes to reach a given checkpoint. See the `eta` variable above for more details.
<br><br/>


# **Helper Functions**

## `update_location()`

The method by which the ETA class determines the car's current location. Currently, the method just reads from a text file, however, this should be replaced with the appropriate code when available.

### **Return Value**
Returns `True` if the update was successful, otherwise it returns `False`.

## `update_checkpoint(lat=None, lon=None, full_scan=True)`

The `update_checkpoint` method will check if the car has passed any checkpoints and use that information in future `get_eta` calls. The method accepts the following parameters:

* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float
* `full_scan` - accepts a boolean

To expand on the `full_scan` parameter, when it is set to `True` the method will use a brute force to check for the closest point on the race route. This point will be used to determine which checkpoints have been passed.

When `full_scan` is set to `false`, the method will only check a geofence surrounding the next checkpoint. If the method finds that the car is within that geofence, then it will automatically increment the checkpoint.

## `find_closest_point(lat, lon)`

The function accepts two mandatory parameters `lat` and `lon`.

* `lat` - accepts latitude of the location as a float
* `lon` - accepts longitude of the location as a float

### **Return Value**
Returns a row of the `route_model` dataframe, which contains information about the point on the race route closest to the given lat/lon pair.

## `get_next_checkpoint_coordinates()`

### **Return Value**
Returns a list containing a lat/lon pair. The lat/lon pair is the coordinates of the next checkpoint.