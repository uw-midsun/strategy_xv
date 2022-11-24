import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import dotenv
import pandas as pd
from elevations.get_elevations import get_elevations




dotenv.load_dotenv()
BING_MAPS_API_KEY = os.getenv("BING_MAPS_API_KEY")




class Test_get_elevations():


    coordinates = [
        (44.0104111274582, -79.67866520101909), 
        (44.028996763626, -79.59455210533561), 
        (44.037352902093524, -79.596693165953), 
        (44.067688969642624, -79.62238589336177), 
        (44.07494094439971, -79.62452695397917), 
        (44.05647962446555, -79.70741658645272)
        ]
    data = get_elevations(coordinates=coordinates, BING_MAPS_API_KEY=BING_MAPS_API_KEY)

    
    def test_latitude(self):
        latitude = self.data["latitude"].to_frame()
        correct_lattitude = pd.DataFrame({"latitude": [44.0104111274582, 44.028996763626, 44.037352902093524, 44.067688969642624, 44.07494094439971, 44.05647962446555]})
        pd.testing.assert_frame_equal(latitude, correct_lattitude)
        

    def test_longitude(self):
        longitude = self.data["longitude"].to_frame()
        correct_longitude = pd.DataFrame({"longitude": [-79.67866520101909, -79.59455210533561, -79.596693165953, -79.62238589336177, -79.62452695397917, -79.70741658645272]})
        pd.testing.assert_frame_equal(longitude, correct_longitude)


    def test_elevation(self):
        elevation = self.data["elevation(m)"].to_frame()
        correct_elevation = pd.DataFrame({"elevation(m)": [195, 207, 183, 189, 190, 207]})
        pd.testing.assert_frame_equal(elevation, correct_elevation)

    
    def test_elevation_gains_to_next(self):
        elevation_gains_to_next = self.data["elevation_gains_to_next(m)"].to_frame()
        correct_elevation_gains_to_next = pd.DataFrame({"elevation_gains_to_next(m)": [12, -24, 6, 1, 17, None]})
        pd.testing.assert_frame_equal(elevation_gains_to_next, correct_elevation_gains_to_next)

