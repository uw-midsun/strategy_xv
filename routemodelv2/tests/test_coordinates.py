import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import pandas as pd
from coordinates.get_coordinates import get_coordinates





class Test_get_coordinates():


    coordinates = [
        (43.81857948416717, -79.40101625627213), 
        (43.82045746557804, -79.3901457521166), 
        (43.81990512423598, -79.38545051088512)
        ]
    interval_upper_bound = 1000
    data = get_coordinates(polyline_coordinates=coordinates, interval_upper_bound=interval_upper_bound)


    def test_polyline_point_index(self):
        polyline_point_index = self.data["polyline_point_index"].to_frame()
        correct_polyline_point_index = pd.DataFrame({"polyline_point_index": [0, 1, 2]})
        pd.testing.assert_frame_equal(polyline_point_index, correct_polyline_point_index)


    def test_latitude(self):
        latitude = self.data["latitude"].to_frame()
        correct_latitude = pd.DataFrame({"latitude": [43.818579, 43.820457, 43.819905]})
        pd.testing.assert_frame_equal(latitude, correct_latitude)


    def test_longitude(self):
        longitude = self.data["longitude"].to_frame()
        correct_longitude = pd.DataFrame({"longitude": [-79.401016, -79.390146, -79.385451]})
        pd.testing.assert_frame_equal(longitude, correct_longitude)


    def test_trip(self):
        trip = self.data["trip(m)"].to_frame()
        correct_trip = pd.DataFrame({"trip(m)": [0, 899.06892, 1281.74487]})
        pd.testing.assert_frame_equal(trip, correct_trip)


    def test_dist_to_next_coordinate(self):
        dist_to_next_coordinate = self.data["dist_to_next_coordinate(m)"].to_frame()
        correct_dist_to_next_coordinate = pd.DataFrame({"dist_to_next_coordinate(m)": [899.06892, 382.67595, None]})
        pd.testing.assert_frame_equal(dist_to_next_coordinate, correct_dist_to_next_coordinate)


    def test_true_bearing_to_next(self):
        true_bearing_to_next = self.data["true_bearing_to_next"].to_frame()
        correct_true_bearing_to_next = pd.DataFrame({"true_bearing_to_next": [76.576401, 99.226778, None]})
        pd.testing.assert_frame_equal(true_bearing_to_next, correct_true_bearing_to_next)


    def test_bearing_to_next_360(self):
        bearing_to_next_360 = self.data["bearing_to_next_360"].to_frame()
        correct_bearing_to_next_360 = pd.DataFrame({"bearing_to_next_360": [76.576401, 99.226778, None]})
        pd.testing.assert_frame_equal(bearing_to_next_360, correct_bearing_to_next_360)


    def test_true_bearing_to_prev(self):
        true_bearing_to_prev = self.data["true_bearing_to_prev"].to_frame()
        correct_true_bearing_to_prev = pd.DataFrame({"true_bearing_to_prev": [None, -103.416072, -80.769971]})
        pd.testing.assert_frame_equal(true_bearing_to_prev, correct_true_bearing_to_prev)


    def test_bearing_to_prev_360(self):
        bearing_to_prev_360 = self.data["bearing_to_prev_360"].to_frame()
        correct_bearing_to_prev_360 = pd.DataFrame({"bearing_to_prev_360": [None, 256.583928, 279.230029]})
        pd.testing.assert_frame_equal(bearing_to_prev_360, correct_bearing_to_prev_360)

    
    def test_general_travel_direction(self):
        general_travel_direction = self.data["general_travel_direction"].to_frame()
        correct_general_travel_direction = pd.DataFrame({"general_travel_direction": ["N77°E", "S9°E", None]})
        pd.testing.assert_frame_equal(general_travel_direction, correct_general_travel_direction)


    def test_turn_bearing(self):
        turn_bearing = self.data["turn_bearing"].to_frame()
        correct_turn_bearing = pd.DataFrame({"turn_bearing": [None, 22.650377, None]})
        pd.testing.assert_frame_equal(turn_bearing, correct_turn_bearing)

    
    def test_turn_type(self):
        turn_type = self.data["turn_type"].to_frame()
        correct_turn_type = pd.DataFrame({"turn_type": [None, "Slight Right", None]})
        pd.testing.assert_frame_equal(turn_type, correct_turn_type)


    def test_relative_turn_angle(self):
        relative_turn_angle = self.data["relative_turn_angle"].to_frame()
        correct_relative_turn_angle = pd.DataFrame({"relative_turn_angle": [None, 22.650377, None]})
        pd.testing.assert_frame_equal(relative_turn_angle, correct_relative_turn_angle)

