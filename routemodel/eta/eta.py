import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import geopy
from geopy.distance import distance as geodist
from geographiclib.geodesic import Geodesic
from routemodel.routemodel import RouteModel
import pandas as pd

# Extra dependencies for Ryan's get_coordinates method
from pyproj import Geod
import math

def get_coordinates(polyline_coordinates: list, interval_upper_bound: int) -> pd.DataFrame:
    """
    get_coordinates is a function that consumes a polygonal chain representation of a route and returns an interpolated route
        and coordinate data in a pandas dataframe
    @param polyline_coordinates: a polygonal chain representation of a route. It is of the form: a list of coordinate tuples
    @param interval_upper_bound: the distance upper bound for the distances between interpolated coordinates
    @return: pandas dataframe with data on: coordinate_point_index, latitudes, longitudes, trip_meters, dist_to_next_coordinate, 
        true_bearing_to_next, bearing_to_next_360, true_bearing_to_prev, bearing_to_prev_360, general_travel_direction, 
        turn_bearings, turn_type, relative_turn_angle
    """


    """
    1) Assert input types and format are correct
    """
    if interval_upper_bound < 10:
        raise TypeError("Due to accuracy issues with the API, the interval upper bound must be at least 10m")
    elif interval_upper_bound < 50:
        print("Due to accuracy issues with the API, it is recommended that the interval upper bound be at least 50m ")
    if len(polyline_coordinates) < 3:
        raise TypeError("coordinate_lst must have at least 3 coordinates")

    
    """
    2) Interpolates each segment into multiple coordinates with the distance between each coordinate less than interval_upper_bound
    - Requires: polyline_coordinates
    - Result: segment_cooridnates
    """
    segment_cooridnates = []
    for i, _ in enumerate(polyline_coordinates[1:], start=1):
        lat_1, long_1 = polyline_coordinates[i-1]
        lat_2, long_2 = polyline_coordinates[i]

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

    
    """
    3) Formats segment_cooridnates into a long list of coordinates
    - Requires: segment_cooridnates
    - Result: coordinate_point_index
    - Result: all_coordinates
    """
    segment_points = {0:0} # {point, index}
    all_coordinates = segment_cooridnates[0].copy()
    for i, segment_coordinate in enumerate(segment_cooridnates[1:], start=1):
        segment_points[len(all_coordinates)-1] = i
        all_coordinates += segment_coordinate[1:]
    segment_points[len(all_coordinates)-1] = len(segment_cooridnates)

    coordinate_point_index = [segment_points[i] if i in segment_points else None for i in range(len(all_coordinates))]


    """
    4) Converts list of coordinates into their lat and long
    - Requires: all_coordinates
    - Result: latitudes
    - Result: longitudes
    """
    latitudes = []
    longitudes = []
    for _, coordinate in enumerate(all_coordinates):
        latitudes.append(coordinate[0])
        longitudes.append(coordinate[1])

    
    """
    5) Finds the distance to the next coordinate, the bearing to the next and previous coordinate
    - Requires: all_coordinates
    - Result: dist_to_next_coordinate
    - Result: trip_meters
    - Result: true_bearing_to_next
    - Result: true_bearing_to_prev
    - Result: bearing_to_next_360
    - Result: bearing_to_prev_360
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


    """
    6) Finds the general traveling direction at the coordinate
    - Requires: general_travel_direction
    - Result: general_travel_direction
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


    """
    7) Determines the type of turn and the turning angle
    - Requires: all_coordinates
    - Result: turn_bearings
    - Result: turn_type
    - Result: relative_turn_angle
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


    """
    8) Builds Pandas DataFrame to return
    - Requires: coordinate_point_index
    - Requires: latitudes
    - Requires: longitudes
    - Requires: trip_meters
    - Requires: dist_to_next_coordinate
    - Requires: true_bearing_to_next
    - Requires: bearing_to_next_360
    - Requires: true_bearing_to_prev
    - Requires: bearing_to_prev_360
    - Requires: general_travel_direction
    - Requires: turn_bearings
    - Requires: turn_type
    - Requires: relative_turn_angle
    - Result: Dataframe
    """
    data = pd.DataFrame({
        "polyline_point_index": coordinate_point_index,
        "latitude": latitudes,
        "longitude": longitudes,
        "trip(m)": trip_meters,
        "dist_to_next_coordinate(m)": dist_to_next_coordinate,
        "true_bearing_to_next": true_bearing_to_next,
        "bearing_to_next_360": bearing_to_next_360,
        "true_bearing_to_prev": true_bearing_to_prev,
        "bearing_to_prev_360": bearing_to_prev_360,
        "general_travel_direction": general_travel_direction,
        "turn_bearing": turn_bearings,
        "turn_type": turn_type,
        "relative_turn_angle": relative_turn_angle,
    })
    return data

class ETA():
    def __init__(self, route, lat=0, lon=0):
        """
            Route refers to the points that model the race path, it can use as many points as necessary
            Checkpoints refer to the condensed race route which has been split into 'x' km increments
        """
        self.lat = lat
        self.lon = lon

        self.route = route

        self.route_model = get_coordinates(polyline_coordinates=route, interval_upper_bound=25)
        self.checkpoint_frequency = 1000 # meters
        self.generate_checkpoints(self.checkpoint_frequency)
        self.current_checkpoint = 0

        self.eta = []
        self.speed = 5 # Speed in km/h

    def build_distance_between_coordinates(self, coordinates: list):
        """
        Determines the distance between coordinate/point n and coordinate/point n+1
        @param coordinates: list of (lat, long) coordinate tuples
        @return: List of n-1 length where the i-th entry represents the distance between coordinate/point n and n+1
        """
        if len(coordinates) < 2:
            raise ValueError("'distance_between_coordinates' function requires at least 2 coordinates")

        distance_between_coordinates = []
        for i, coordinate in enumerate(coordinates[1:], start=1):
            distance = round(geodist(coordinates[i-1], coordinates[i]).m, 2)
            distance_between_coordinates.append(distance/1000)

        return distance_between_coordinates
    
    def generate_checkpoints(self, freq):
        """
        Generates 'checkpoints' which are {freq} meters apart where weather and other API calls can be made from
        @param freq: the distance in meters between each generated checkpoint
        @return: List of coordinates representing each of the checkpoints
        """

        self.checkpoint_coords = [] 
        self.checkpoint_index = []
        checkpoint = [] # Stores the index of the last checkpoint passed for any given route model point

        lst_checkpoint = -1

        for index, row in self.route_model.iterrows():
            cur_checkpoint = int(row['trip(m)'] // freq)
            if cur_checkpoint != lst_checkpoint: 
                self.checkpoint_coords.append([row['latitude'], row['longitude']])
                self.checkpoint_index.append(index)
            
            checkpoint.append(cur_checkpoint)
            lst_checkpoint = cur_checkpoint

        self.route_model['checkpoint'] = checkpoint
        
        return self.checkpoint_coords

    def update_location(self):
        try:
            current_loc_path = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, "current_location.txt"))
            with open(current_loc_path, "r") as f:
                lat, lon = map(float, f.readline().split(', '))
                self.lat = lat
                self.lon = lon
                f.close()
            return True
        except:
            print("(eta.py) There was an issue with updating the location.\
            \nFor reference, the program attempted to open", os.path.join(os.path.abspath(__file__), os.pardir, "current_location.txt"))
            return False

    def check_geofence(self, clat, clon, plat, plon):
        '''
        Checks if the given lat/lon is within a 600m box of a specified point
        '''
        wb = geodist(kilometers = 0.3).destination(point=geopy.Point(plat, plon), bearing = 270).longitude
        sb = geodist(kilometers = 0.3).destination(point=geopy.Point(plat, plon), bearing = 180).latitude
        eb = geodist(kilometers = 0.3).destination(point=geopy.Point(plat, plon), bearing = 90).longitude
        nb = geodist(kilometers = 0.3).destination(point=geopy.Point(plat, plon), bearing = 0).latitude

        c1 = (sb < clat) and (clat < nb)
        c2 = (wb < clon) and (clon < eb)

        return (c1 and c2)

    def find_closest_point(self, lat, lon):
        '''
        The function takes in a coordinate point (lat/lon) and finds the closest point to it inside the route model 
        @param lat: float representing the latitude
        @param lon: float representing the longitude
        @return: a row of the route_model dataframe containing information about the closest point on the race route
        '''

        distances = self.route_model.apply(lambda row: geodist((lat, lon), (row['latitude'], row['longitude'])).meters, axis=1)
        return self.route_model.iloc[distances.idxmin()]

    def update_checkpoint(self, lat = None, lon = None, full_scan = True):
        '''
        update_checkpoint() is a function that determines which segment of the race the car is on based on the current lat/lon.
        When full_scan == true, a brute force method is used to check for the closest point.

        @param lat: float representing the latitude, an automatic location update is done if it is not provided
        @param lon: float representing the longitude, an automatic location update is done if it is not provided
        @param full_scan: boolean that determines which method is used to update the checkpoint
        '''
        # If update racepoint is called with lat/lon given
        if lat and lon:
            self.lat = lat
            self.lon = lon
        else:
            self.update_location()

        # Brute Force on larger points dataset
        if full_scan:
            closest_point = self.find_closest_point(self.lat, self.lon)
            self.current_checkpoint = closest_point['checkpoint']
            print(self.current_checkpoint)

        else:
            i = self.current_checkpoint
            if i+1 < len(self.checkpoint_coords):
                plat, plon = self.checkpoint_coords[i+1]
                if self.check_geofence(self.lat, self.lon, plat, plon) == True:
                    self.current_checkpoint = i+1

    def get_next_checkpoint_coordinates(self):
        """
        @return: a list containing a lat/lon pair with the coordinates of the next checkpoint
        """
        i = self.current_checkpoint
        if i+1 < len(self.current_checkpoint):
            return self.checkpoint_coords[i+1]
        else:
            return []

    def get_checkpoints_coordinates(self):
        return self.checkpoints_coords
        
    def get_eta(self):
        """
        @return: a list of float values representing the time it takes to reach the checkpoints
        """
        
        next_closest_checkpoint = self.current_checkpoint+1
        n = len(self.checkpoint_coords)
        eta = [-1 for _ in range(n)]

        if next_closest_checkpoint >= n: 
            self.eta = eta
            return self.eta

        print(self.route_model)

        slat = self.lat
        slon = self.lon
        elat = self.checkpoint_coords[next_closest_checkpoint][0]
        elon = self.checkpoint_coords[next_closest_checkpoint][1]

        dist_to_next_checkpoint = geodist((slat, slon), (elat, elon)).meters
        # Unit conversion is to put meters into kilometers and time into minutes
        eta[next_closest_checkpoint] =  (dist_to_next_checkpoint/1000) / self.speed * 60 

        for future_checkpoint in range(next_closest_checkpoint+1, n):
            a = self.checkpoint_index[next_closest_checkpoint]
            b = self.checkpoint_index[future_checkpoint]

            # Unit conversion is to put meters into kilometers and time into minutes
            eta_next_to_future = ((self.route_model.iloc[b].loc['trip(m)'] - self.route_model.iloc[a].loc['trip(m)'])/1000) / self.speed * 60
            eta[future_checkpoint] = eta[next_closest_checkpoint] + eta_next_to_future

        self.eta = eta
        return eta
