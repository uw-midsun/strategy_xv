import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))

from dotenv import load_dotenv
import pandas as pd
from elevations.elevations import RouteElevation, CoordinateElevation

load_dotenv()


"""
- Test RouteElevation using the self.route in ./assets/tutorial1.png
- Test CoordinateElevation using the self.route in ./assets/tutorial1.png
- Plotting graph method is not tested
- Make sure API Key is here
"""
BING_MAPS_API_KEY = os.environ['BING_MAPS_API_KEY']

class Test_RouteElevation():
    coordinates = [
        (44.0104111274582, -79.67866520101909), 
        (44.028996763626, -79.59455210533561), 
        (44.037352902093524, -79.596693165953), 
        (44.067688969642624, -79.62238589336177), 
        (44.07494094439971, -79.62452695397917), 
        (44.05647962446555, -79.70741658645272)
        ]
    route = RouteElevation(
        coordinates=coordinates, 
        BING_MAPS_API_KEY=BING_MAPS_API_KEY,
        sample_frequency_upper_bound=500, 
        offset=0, 
        debug=False
        )


    def test_distance_between_coordinates(self):
        distance_between_coordinates = self.route.build_distance_between_coordinates(self.route._coordinates)
        correct_distance_between_coordinates = [7053.25, 944.2, 3949.8, 823.85, 6950.51]
        assert distance_between_coordinates == correct_distance_between_coordinates


    def test_sample_distances_between_coordinates(self):
        sample_distances_between_coordinates = self.route.build_sample_frequency_distances_between_coordinates(self.route._distance_between_coordinates, self.route._sample_frequency_upper_bound)
        correct_sample_distances_between_coordinates = [(16, 470.22), (3, 472.1), (9, 493.73), (3, 411.93), (15, 496.47)]
        assert sample_distances_between_coordinates == correct_sample_distances_between_coordinates


    def test_query_coordinate_pairs(self):
        query_coordinate_pairs = self.route.build_query_coordinate_pairs(self.route._coordinates)
        correct_query_coordinate_pairs = [
            '44.0104111274582,-79.67866520101909,44.028996763626,-79.59455210533561', 
            '44.028996763626,-79.59455210533561,44.037352902093524,-79.596693165953', 
            '44.037352902093524,-79.596693165953,44.067688969642624,-79.62238589336177', 
            '44.067688969642624,-79.62238589336177,44.07494094439971,-79.62452695397917', 
            '44.07494094439971,-79.62452695397917,44.05647962446555,-79.70741658645272'
            ]
        assert query_coordinate_pairs == correct_query_coordinate_pairs


    def test_elevation_data_between_coordinate_pairs(self):
        elevation_data_between_coordinate_pairs = self.route.build_elevation_data_between_coordinate_pairs(self.route._query_coordinate_pairs, self.route._sample_distances_between_coordinates)
        correct_elevation_data_between_coordinate_pairs = [
            [195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207], 
            [207, 187, 183], 
            [183, 180, 180, 181, 182, 203, 194, 191, 189], 
            [189, 189, 190], 
            [190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207]
            ]
        assert elevation_data_between_coordinate_pairs == correct_elevation_data_between_coordinate_pairs


    def test_x_axis_distance(self):
        x_axis_distance = self.route.build_x_axis_distance(self.route._sample_distances_between_coordinates, self.route._offset)
        correct_x_axis_distance = [
            0, 470, 940, 1410, 1880, 2351, 2821, 3291, 3761, 4231, 4702, 5172, 5642, 6112, 6583, 7053, 7525, 7997, 
            8491, 8984, 9478, 9972, 10466, 10959, 11453, 11947, 12359, 12771, 13267, 13764, 14260, 14757, 15253, 
            15750, 16246, 16742, 17239, 17735, 18232, 18728, 19225, 19721
            ]
        assert x_axis_distance == correct_x_axis_distance


    def test_y_axis_elevations(self):
        y_axis_elevations = self.route.build_y_axis_elevations(self.route._elevation_data_between_coordinate_pairs)
        correct_y_axis_elevations = [
            195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207, 187, 183, 180, 180, 181, 
            182, 203, 194, 191, 189, 189, 190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207
            ]
        assert y_axis_elevations == correct_y_axis_elevations


    def test_x_axis_segments(self):
        x_axis_segments = self.route.build_x_axis_segments(self.route._x_axis_distance, self.route._sample_distances_between_coordinates)
        correct_x_axis_segments = [0, 7053, 7997, 11947, 12771, 19721]
        assert x_axis_segments == correct_x_axis_segments


    def test_y_axis_segments(self):
        y_axis_segments = self.route.build_y_axis_segments(self.route._y_axis_elevations, self.route._sample_distances_between_coordinates)
        correct_y_axis_segments = [195, 207, 183, 189, 190, 207]
        assert y_axis_segments == correct_y_axis_segments


    def test_get_elevation_all(self):
        distance, elevation = self.route.get_elevations()
        correct_distance = [
            0, 470, 940, 1410, 1880, 2351, 2821, 3291, 3761, 4231, 4702, 5172, 5642, 6112, 6583, 7053, 7525, 7997, 8491, 
            8984, 9478, 9972, 10466, 10959, 11453, 11947, 12359, 12771, 13267, 13764, 14260, 14757, 15253, 15750, 16246, 
            16742, 17239, 17735, 18232, 18728, 19225, 19721
            ]
        correct_elevation = [
            195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207, 187, 183, 180, 180, 181, 182, 
            203, 194, 191, 189, 189, 190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207
            ]
        assert distance == correct_distance
        assert elevation == correct_elevation


    def test_get_elevation_index_0_to_3(self):
        distance, elevation = self.route.get_elevations(0,3)
        correct_distance = [
            0, 470, 940, 1410, 1880, 2351, 2821, 3291, 3761, 4231, 4702, 5172, 5642, 6112, 6583, 7053, 7525, 7997, 
            8491, 8984, 9478, 9972, 10466, 10959, 11453, 11947
            ]
        correct_elevation = [
            195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207, 187, 183, 180, 180,
            181, 182, 203, 194, 191, 189
            ]
        assert distance == correct_distance
        assert elevation == correct_elevation


    def test_get_elevation_index_4_to_5(self):
        distance, elevation = self.route.get_elevations(4,5)
        correct_distance = [
            12771, 13267, 13764, 14260, 14757, 15253, 15750, 16246, 16742, 17239, 17735, 18232, 18728, 19225, 19721
            ]
        correct_elevation = [190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207]
        assert distance == correct_distance
        assert elevation == correct_elevation


    def test_get_dataframe_all(self):
        data = self.route.get_dataframe()
        correct_distance = [
            0, 470, 940, 1410, 1880, 2351, 2821, 3291, 3761, 4231, 4702, 5172, 5642, 6112, 6583, 7053, 7525, 7997, 8491, 
            8984, 9478, 9972, 10466, 10959, 11453, 11947, 12359, 12771, 13267, 13764, 14260, 14757, 15253, 15750, 16246, 
            16742, 17239, 17735, 18232, 18728, 19225, 19721
            ]
        correct_elevation = [
            195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207, 187, 183, 180, 180, 181, 182, 
            203, 194, 191, 189, 189, 190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207
            ]
        correct_dataframe = pd.DataFrame({"distance":correct_distance, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)


    def test_get_dataframe_index_0_to_3(self):
        data = self.route.get_dataframe(0,3)
        correct_distance = [
            0, 470, 940, 1410, 1880, 2351, 2821, 3291, 3761, 4231, 4702, 5172, 5642, 6112, 6583, 7053, 7525, 7997, 
            8491, 8984, 9478, 9972, 10466, 10959, 11453, 11947
            ]
        correct_elevation = [
            195, 186, 184, 187, 188, 183, 191, 186, 183, 184, 181, 184, 186, 185, 199, 207, 187, 183, 180, 180,
            181, 182, 203, 194, 191, 189
            ]
        correct_dataframe = pd.DataFrame({"distance":correct_distance, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)


    def test_get_dataframe_index_4_to_5(self):
        data = self.route.get_dataframe(4,5)
        correct_distance = [
            12771, 13267, 13764, 14260, 14757, 15253, 15750, 16246, 16742, 17239, 17735, 18232, 18728, 19225, 19721
            ]
        correct_elevation = [190, 184, 187, 187, 194, 196, 203, 204, 222, 220, 220, 206, 202, 205, 207]
        correct_dataframe = pd.DataFrame({"distance":correct_distance, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)





class Test_CoordinateElevation():
    coordinates = [
        (44.0104111274582, -79.67866520101909), 
        (44.028996763626, -79.59455210533561), 
        (44.037352902093524, -79.596693165953), 
        (44.067688969642624, -79.62238589336177), 
        (44.07494094439971, -79.62452695397917), 
        (44.05647962446555, -79.70741658645272)
        ]
    route = CoordinateElevation(
        coordinates=coordinates, 
        BING_MAPS_API_KEY=BING_MAPS_API_KEY,
        debug=False
        )

    
    def test_compress_coordinates(self):
        compressed_coordinates = self.route.compress_coordinates(self.route._coordinates)
        correct_compressed_coordiantes = ["2h1507lp2InxnnpGv6ljCw-587Bxz61Bpuz8jG"]
        assert compressed_coordinates == correct_compressed_coordiantes


    def test_build_elevation_data(self):
        coordinates_elevations_data = self.route.build_elevation_data(self.route._compressed_coordinates_lst)
        correct_coordinates_elevations_data =  [195, 207, 183, 189, 190, 207]
        assert coordinates_elevations_data == correct_coordinates_elevations_data


    def test_get_elevation_all(self):
        coordinates, elevation = self.route.get_elevations()
        correct_coordinates = self.route._coordinates
        correct_elevation = [195, 207, 183, 189, 190, 207]
        assert coordinates == correct_coordinates
        assert elevation == correct_elevation


    def test_get_elevation_index_0_to_3(self):
        coordinates, elevation = self.route.get_elevations(0,3)
        correct_coordinates = self.route._coordinates[0:3+1]
        correct_elevation = [195, 207, 183, 189]
        assert coordinates == correct_coordinates
        assert elevation == correct_elevation


    def test_get_elevation_index_4_to_5(self):
        coordinates, elevation = self.route.get_elevations(4,5)
        correct_coordinates = self.route._coordinates[4:5+1]
        correct_elevation = [190, 207]
        assert coordinates == correct_coordinates
        assert elevation == correct_elevation


    def test_get_dataframe_all(self):
        data = self.route.get_dataframe()
        correct_latitude = [coordinate[0] for coordinate in self.route._coordinates]
        correct_longitude = [coordinate[1] for coordinate in self.route._coordinates]
        correct_elevation = [195, 207, 183, 189, 190, 207]

        correct_dataframe = pd.DataFrame({"latitude":correct_latitude, "longitude":correct_longitude, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)


    def test_get_dataframe_index_0_to_3(self):
        data = self.route.get_dataframe(0,3)
        correct_latitude = [coordinate[0] for coordinate in self.route._coordinates[0:3+1]]
        correct_longitude = [coordinate[1] for coordinate in self.route._coordinates[0:3+1]]
        correct_elevation = [195, 207, 183, 189]
        correct_dataframe = pd.DataFrame({"latitude":correct_latitude, "longitude":correct_longitude, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)


    def test_get_dataframe_index_4_to_5(self):
        data = self.route.get_dataframe(4,5)
        correct_latitude = [coordinate[0] for coordinate in self.route._coordinates[4:5+1]]
        correct_longitude = [coordinate[1] for coordinate in self.route._coordinates[4:5+1]]
        correct_elevation = [190, 207]
        correct_dataframe = pd.DataFrame({"latitude":correct_latitude, "longitude":correct_longitude, "elevation":correct_elevation})
        pd.testing.assert_frame_equal(data, correct_dataframe)
