from geographiclib.geodesic import Geodesic
from pyproj import Geod
import math
import pandas as pd
import warnings




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
        warnings.warn("Due to accuracy issues with the API, it is recommended that the interval upper bound be at least 50m\n")
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




if __name__ == "__main__":
    pass

