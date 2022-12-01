from geographiclib.geodesic import Geodesic
from pyproj import Geod
import math
import pandas as pd
import warnings
from typing import List, Tuple



class RouteModel():

    def __init__(self, coordinate_lst_input: List[Tuple[float]], interval_upper_bound: int = 100):
        """
        @param coordinate_lst_input: polygonal chain representation of the route
        @param interval_upper_bound: uppper bound for the distance between coordinates
        """
        self._coordinate_lst_input = coordinate_lst_input
        self._interval_upper_bound = interval_upper_bound

        self._segment_cooridnates = None

        self._coordinate_point_index = None
        self._all_coordinates = None

        self._latitudes = None
        self._longitudes = None

        self._dist_to_next_coordinate = None
        self._true_bearing_to_next = None
        self._true_bearing_to_prev = None
        self._bearing_to_next_360 = None
        self._bearing_to_prev_360 = None

        self._general_travel_direction = None

        self._turn_bearings = None
        self._turn_type = None
        self._relative_turn_angle = None

        self._data = None
        
        if self._interval_upper_bound < 10:
            raise TypeError("Due to accuracy issues with the API, the interval upper bound must be at least 10m\n")
        elif self._interval_upper_bound < 50:
            warnings.warn("Due to accuracy issues with the API, it is recommended that the interval upper bound be at least 50m\n")

        if len(self._coordinate_lst_input) < 3:
            raise TypeError("coordinate_lst must have at least 3 coordinates")

        self.build_data()


    def build_data(self):
        """
        build_data: Runs the algorithm
        """
        self._segment_cooridnates = self.build_segment_cooridnates(self._coordinate_lst_input, self._interval_upper_bound)

        segment_and_coordinate_data = self.build_segment_points(self._segment_cooridnates)
        self._coordinate_point_index = segment_and_coordinate_data["coordinate_point_index"]
        self._all_coordinates = segment_and_coordinate_data["all_coordinates"]

        latlon_data = self.build_latitudes_longitudes(self._all_coordinates)
        self._latitudes = latlon_data["latitudes"]
        self._longitudes = latlon_data["longitudes"]

        dist_and_bearing_data = self.build_distance_and_bearing(self._all_coordinates)
        self._dist_to_next_coordinate = dist_and_bearing_data["dist_to_next_coordinate"]
        self._trip_meters = dist_and_bearing_data["trip_meters"]
        self._true_bearing_to_next = dist_and_bearing_data["true_bearing_to_next"]
        self._true_bearing_to_prev = dist_and_bearing_data["true_bearing_to_prev"]
        self._bearing_to_next_360 = dist_and_bearing_data["bearing_to_next_360"]
        self._bearing_to_prev_360 = dist_and_bearing_data["bearing_to_prev_360"]

        self._general_travel_direction = self.build_general_travel_direction(self._bearing_to_next_360)

        turn_data = self.build_turn_data(self._all_coordinates, self._true_bearing_to_next)
        self._turn_bearings = turn_data["turn_bearings"]
        self._turn_type = turn_data["turn_type"]
        self._relative_turn_angle = turn_data["relative_turn_angle"]

        self._data = self.build_dataframe()


    def build_segment_cooridnates(self, coordinate_lst_input: List[Tuple[float]], interval_upper_bound: int): 
        """
        build_segment_cooridnates: interpolates each segment into multiple coordinates with the distance between each coordinate
            less than interval_upper_bound
        @param coordinate_lst_input: polygonal chain representation of the route
        @param interval_upper_bound: uppper bound for the distance between coordinates
        @return: returns a list of lists that contains the coordinates for each segment in the route/polygonal chain
        """
        segment_cooridnates = []
        for i, _ in enumerate(coordinate_lst_input[1:], start=1):
            lat_1, long_1 = coordinate_lst_input[i-1]
            lat_2, long_2 = coordinate_lst_input[i]

            geo_data = Geodesic.WGS84.Inverse(lat_1, long_1, lat_2, long_2)
            dist = geo_data['s12'] # https://geographiclib.sourceforge.io/1.52/python/interface.html
            intervals_num = math.ceil(dist/interval_upper_bound)-1
            
            if intervals_num == 0:
                segment_cooridnates.append([(lat_1, long_1), (lat_2, long_2)])
            else:
                g = Geod(ellps="WGS84")
                longlats = g.npts(long_1, lat_1, long_2, lat_2, intervals_num) # be careful here because the lat and longs order is switched
                data = [(lat_1, long_1)] + [(lat, long) for long, lat in longlats] + [(lat_2, long_2)]
                segment_cooridnates.append(data)

        return segment_cooridnates


    def build_segment_points(self, segment_cooridnates: List[List[Tuple[float]]]):
        """
        build_segment_points: Formats segment_cooridnates into a long list of coordinates
        @param segment_cooridnates: a list of lists that contains the coordinates for each segment in the route/polygonal chain
        @return coordinate_point_index: a list of the polygonal chain points and their index
        @return all_coordinates: long list of coordinates that represents the route
        """
        segment_points = {0:0} # {point, index}
        all_coordinates = segment_cooridnates[0].copy()
        for i, segment_coordinate in enumerate(segment_cooridnates[1:], start=1):
            segment_points[len(all_coordinates)-1] = i
            all_coordinates += segment_coordinate[1:]
        segment_points[len(all_coordinates)-1] = len(segment_cooridnates)

        coordinate_point_index = [segment_points[i] if i in segment_points else None for i in range(len(all_coordinates))]
        
        return {"coordinate_point_index":coordinate_point_index, "all_coordinates":all_coordinates}


    def build_latitudes_longitudes(self, all_coordinates: List[Tuple[float]]):
        """
        build_latitudes_longitudes: Converts list of coordinates into their lat and long
        @param all_coordinates: long list of coordinates that represents the route
        @return latitudes: a list of all the latitudes in all_coordinates
        @return longitudes: a list of all the longitudes in all_coordinates
        """
        latitudes = []
        longitudes = []
        for _, coordinate in enumerate(all_coordinates):
            latitudes.append(coordinate[0])
            longitudes.append(coordinate[1])

        return {"latitudes":latitudes, "longitudes":longitudes}


    def build_distance_and_bearing(self, all_coordinates: List[Tuple[float]]):
        """"
        build_distance_and_bearing: finds the distance to the next coordinate, the bearing to the next and previous coordinate
        @param all_coordinates: long list of coordinates that represents the route
        @return dist_to_next_coordinate: list of distances between coordinates
        @return trip_meters: cumulative number of meters completed (at this point relative to the start of the route)
        @return true_bearing_to_next: list of bearings to next coordinates to true north
        @return true_bearing_to_prev: list of bearings to prev coordinates to true north
        @return bearing_to_next_360: list of bearings to next coordinates in 360 degrees
        @return bearing_to_prev_360: list of bearings to prev coordinates in 360 degrees
        """
        dist_to_next_coordinate = []
        trip_meters = [0]
        true_bearing_to_next = []
        true_bearing_to_prev = [None]
        for i, _ in enumerate(all_coordinates[:-1]):
            lat_1, long_1 = all_coordinates[i]
            lat_2, long_2 = all_coordinates[i+1]
            geo_data = Geodesic.WGS84.Inverse(lat_1, long_1, lat_2, long_2) # return values: https://geographiclib.sourceforge.io/1.52/python/interface.html
            dist_to_next_coordinate.append(geo_data["s12"]) # dist between coordinates
            trip_meters.append(trip_meters[-1] + geo_data["s12"]) # trip dist so far
            true_bearing_to_next.append(geo_data["azi1"]) # bearing to next
            true_bearing_to_prev.append(geo_data["azi2"]+180 if geo_data["azi2"]+180 <= 180 else geo_data["azi2"]-180) # bearing to prev
        dist_to_next_coordinate.append(None)
        true_bearing_to_next.append(None)

        bearing_to_next_360 = [i+360 if (i is not None and i < 0) else i for i in true_bearing_to_next]
        bearing_to_prev_360 = [i+360 if (i is not None and i < 0) else i for i in true_bearing_to_prev]

        return {
            "dist_to_next_coordinate": dist_to_next_coordinate, 
            "trip_meters": trip_meters,
            "true_bearing_to_next": true_bearing_to_next, 
            "true_bearing_to_prev": true_bearing_to_prev,
            "bearing_to_next_360": bearing_to_next_360,
            "bearing_to_prev_360": bearing_to_prev_360
            }


    def build_general_travel_direction(self, bearing_to_next_360: List[float]):
        """"
        build_general_travel_direction: finds the general traveling direction at the coordinate
        @param bearing_to_next_360: list of bearings to next coordinates in 360 degrees
        @return: alist of the general traveling direction at the coordinate
        """
        general_travel_direction = []
        for bearing in bearing_to_next_360:
            if bearing is None:
                general_travel_direction.append(None)
            elif bearing == 0 or bearing == 360:
                general_travel_direction.append("N")
            elif bearing == 90:
                general_travel_direction.append("E")
            elif bearing == 180:
                general_travel_direction.append("S")
            elif bearing == 270:
                general_travel_direction.append("W")
            elif 0 < bearing < 90:
                general_travel_direction.append(f"N{bearing:.0f}{chr(176)}E")
            elif 90 < bearing < 180:
                general_travel_direction.append(f"S{bearing-90:.0f}{chr(176)}E")
            elif 180 < bearing < 270:
                general_travel_direction.append(f"S{bearing-180:.0f}{chr(176)}W")
            elif 270 < bearing < 360:
                general_travel_direction.append(f"N{bearing-270:.0f}{chr(176)}W")

        return general_travel_direction


    def build_turn_data(self, all_coordinates, true_bearing_to_next: List[float]):
        """
        build_turn_data: determines the type of turn and the turning angle
        @param all_coordinates: long list of coordinates that represents the route
        @param true_bearing_to_next: list of bearings to next coordinates to true north
        @return turn_bearings: the relative turn bearing,
        @return turn_type: a list of type of turn at the coordinate,
        @return relative_turn_angle: the relative turn angle (formatted)
        """
        turn_bearings = [None]
        for i, _ in enumerate(all_coordinates[1:-1], start=1):
            bearing1 = true_bearing_to_next[i-1]
            bearing2 = true_bearing_to_next[i]
            if bearing2-bearing1 > 180:
                 turn_bearings.append(bearing2-bearing1-360)
            elif bearing2-bearing1 < -180:
                turn_bearings.append(bearing2-bearing1+360)
            else:
                turn_bearings.append(bearing2-bearing1)
        turn_bearings.append(None)

        turn_type = []
        relative_turn_angle = []
        for bearing in turn_bearings:
            if bearing is None or abs(bearing) < 1:
                turn_type.append(None)
                relative_turn_angle.append(None)
                continue
            elif -60 <= bearing <= 60: # within 60 degrees is a slight turn
                turn_type.append("Slight Left" if bearing < 0 else "Slight Right")
            elif -120 <= bearing <= 120: # within 60-120 degrees is a standard turn
                turn_type.append("Standard Left" if bearing < 0 else "Standard Right")
            else: # greater than 120 degrees is a hook turn
                turn_type.append("Hook Left" if bearing < 0 else "Hook Right")
            relative_turn_angle.append(abs(bearing))

        return {
            "turn_bearings": turn_bearings,
            "turn_type": turn_type,
            "relative_turn_angle": relative_turn_angle
        }


    def build_dataframe(self): 
        """
        build_dataframe: builds Pandas DataFrame
        @return: DataFrame of the route data
        """
        data = pd.DataFrame({
            "polyline_point_index": self._coordinate_point_index,
            "latitude": self._latitudes,
            "longitude": self._longitudes,
            "trip_meters": self._trip_meters,
            "dist_to_next_coordinate": self._dist_to_next_coordinate, # in meters
            "true_bearing_to_next": self._true_bearing_to_next,
            "bearing_to_next_360": self._bearing_to_next_360,
            "true_bearing_to_prev": self._true_bearing_to_prev,
            "bearing_to_prev_360": self._bearing_to_prev_360,
            "general_travel_direction": self._general_travel_direction,
            "turn_bearing": self._turn_bearings,
            "turn_type": self._turn_type,
            "relative_turn_angle": self._relative_turn_angle,
        }).fillna('')
        return data


    def get_data(self):
        """
        build_dataframe: gives user route data DataFrame
        @return: DataFrame of the route data
        """
        if self._data is None:
            self.build_data()
        return self._data


    def get_csv(self, filename: str):
        """
        build_dataframe: saves user route data as csv
        @param filename: name of saved file
        """
        data = self.get_data()
        format_filename = f"{filename}.csv" if ".csv" not in filename else filename
        data.to_csv(format_filename)


    def get_elevations_list(self):
        """
        get_elevations_list: gives user a list of all coordinate tuples
        @return: list of tuples, where each tuple represents a (latitude, longitude) coordinate
        """
        data = self.get_data()
        latitudes = data["latitude"].to_list()
        longitudes = data["longitude"].to_list()
        return list(zip(latitudes, longitudes))



if __name__ == "__main__":
    pass
