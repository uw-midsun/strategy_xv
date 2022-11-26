import os
import dotenv
import numpy as np
import pandas as pd

from RouteClass import RouteClass
from coordinates.get_coordinates import get_coordinates
from elevations.get_elevations import get_elevations
import time
t0 = time.time()

"""
API KEYS
"""
dotenv.load_dotenv()
# BING_MAPS_API_KEY = "" # Manual option
BING_MAPS_API_KEY = os.getenv("BING_MAPS_API_KEY")


"""
Step 1: Initiate RouteClass wrapper for our route
"""
polyline_coordinates = [
    (43.467879339595996, -80.56616840836313),
    (43.47883157462026, -80.53538493288134),
    (43.473830662244815, -80.53170344584917),
    (43.471525236984746, -80.53744468397863),
    (43.4644417537584, -80.54157837541729),
    (43.46348360838345, -80.53993555488016),
    (43.46266401802443, -80.53908339764159)
    ]
interval_upper_bound = 100
route = RouteClass(polyline_coordinates=polyline_coordinates, interval_upper_bound=interval_upper_bound)


"""
Step 2: Interpolate coordinates and coordinate info for our route
"""
polyline_coordinates = route.polyline_coordinates
interval_upper_bound = route.interval_upper_bound

coordinates = get_coordinates(polyline_coordinates=polyline_coordinates, interval_upper_bound=interval_upper_bound)
route.append_data(coordinates)
# print(route.data())
# route.get_csv("route0")


"""
Step 3: Get elevation info for our route
"""
latitude = route.data()["latitude"]
longitude = route.data()["longitude"]
coordinates = list(zip(latitude, longitude))

elevations = get_elevations(coordinates=coordinates, BING_MAPS_API_KEY=BING_MAPS_API_KEY)
route.append_data(elevations)
# print(route.data())
# route.get_csv("route1")