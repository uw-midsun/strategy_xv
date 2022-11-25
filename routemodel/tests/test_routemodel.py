import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import math
from routemodel.routemodel import RouteModel





class Test_RouteModel():
    coordinate_lst_input = [
        (43.81857948416717, -79.40101625627213), 
        (43.82045746557804, -79.3901457521166), 
        (43.81990512423598, -79.38545051088512)
        ]
    interval_upper_bound = 1000
    route = RouteModel(coordinate_lst_input, interval_upper_bound) 



    def is_almost_equal(self, lst_a, lst_b):
        """
        Checks if the values in lst_a are almost equal to the values
        in lst_b, includind None values"""
        assert len(lst_a) == len(lst_b)
        for i in range(len(lst_a)):
            a = lst_a[i]
            b = lst_b[i]
            try:
                assert math.isClose(a, b)
            except:
                a == b # NoneTypes



    def test_polyline_point_index(self):
        polyline_point_index = self.route._coordinate_point_index
        correct_polyline_point_index = [0, 1, 2]
        assert polyline_point_index == correct_polyline_point_index


    def test_latitude(self):
        latitude = self.route._latitudes
        correct_latitude = [43.81857948416717, 43.82045746557804, 43.81990512423598]
        self.is_almost_equal(latitude, correct_latitude)


    def test_longitude(self):
        longitude = self.route._longitudes
        correct_longitude = [-79.40101625627213, -79.3901457521166, -79.38545051088512]
        self.is_almost_equal(longitude, correct_longitude)


    def test_trip_meters(self):
        trip_meters = self.route._trip_meters
        correct_trip_meters = [0, 899.06892, 1281.74487]
        self.is_almost_equal(trip_meters, correct_trip_meters)

    
    def test_dist_to_next_coordinate(self):
        dist_to_next_coordinate = self.route._dist_to_next_coordinate
        correct_dist_to_next_coordinate = [899.06892, 382.67595, None]
        self.is_almost_equal(dist_to_next_coordinate, correct_dist_to_next_coordinate)


    def test_true_bearing_to_next(self):
        true_bearing_to_next = self.route._true_bearing_to_next
        correct_true_bearing_to_next = [76.576401, 99.226778, None]
        self.is_almost_equal(true_bearing_to_next, correct_true_bearing_to_next)


    def test_bearing_to_next_360(self):
        bearing_to_next_360 = self.route._bearing_to_next_360
        correct_bearing_to_next_360 = [76.576401, 99.226778, None]
        self.is_almost_equal(bearing_to_next_360, correct_bearing_to_next_360)


    def test_true_bearing_to_prev(self):
        true_bearing_to_prev = self.route._true_bearing_to_prev
        correct_true_bearing_to_prev = [None, -103.416072, -80.769971]
        self.is_almost_equal(true_bearing_to_prev, correct_true_bearing_to_prev)


    def test_bearing_to_prev_360(self):
        bearing_to_prev_360 = self.route._bearing_to_prev_360
        correct_bearing_to_prev_360 = [None, 256.583928, 279.230029]
        self.is_almost_equal(bearing_to_prev_360, correct_bearing_to_prev_360)


    def test_general_travel_direction(self):
        general_travel_direction = self.route._general_travel_direction
        correct_general_travel_direction = ["N77°E", "S9°E", None]
        self.is_almost_equal(general_travel_direction, correct_general_travel_direction)


    def test_turn_bearing(self):
        turn_bearing = self.route._turn_bearings
        correct_turn_bearing = [None, 22.65037, None]
        self.is_almost_equal(turn_bearing, correct_turn_bearing)


    def test_turn_type(self):
        turn_type = self.route._turn_type
        correct_turn_type = [None, "Slight Right", None]
        self.is_almost_equal(turn_type, correct_turn_type)


    def test_relative_turn_angle(self):
        relative_turn_angle = self.route._relative_turn_angle
        correct_turn_angle = [None, 22.65037, None]
        self.is_almost_equal(relative_turn_angle, correct_turn_angle)

    def test_get_elevations_list(self):
        elevations = self.route.get_elevations_list()
        correct_elevations = [(43.81857948416717,-79.40101625627213), (43.82045746557804, -79.3901457521166), (43.81990512423598, -79.38545051088512)]
        self.is_almost_equal(elevations, correct_elevations)
