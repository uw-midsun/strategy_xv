import os
import numpy as np
import pandas as pd




class RouteMappingError(Exception):
    pass


def map_routebook_data(trip_distance_list, routebook_filepath):
    """
    map_routebook_data
    """


    """
    1) Get routebook data and clean/remove empty strings
    """
    routebook = pd.read_csv(routebook_filepath)
    routebook.replace(r'^\s*$', np.nan, regex=True, inplace = True)


    """
    2) Reformat the routebook data
    - Remove unused columns
    - Rename columns
    - Convert data to SI units
    """
    del routebook["Int"]
    routebook.rename(inplace=True, columns={
        "Step": "step",
        "Trip": "routebook_trip(m)",
        "Major Turns/Instructions": "instructions",
        "Landmarks/Notes": "landmarks_notes",
        "Ln": "lanes",
        "Spd": "speed_limit(m/s)",
        "Shoulder": "shoulder",
        "Services": "services"
    })
    routebook["routebook_trip(m)"] = routebook["routebook_trip(m)"].apply(lambda x: x*1609.344) # miles to meters
    routebook["speed_limit(m/s)"] = routebook["speed_limit(m/s)"].map(float).apply(lambda x: x*0.44704) # mph to m/s


    """
    3) Index the routebook data to the RouteClass route/data by finding the closest recorded coordinate (from RouteClass)
    to each datapoint in the routebook using the trip(m) difference
    """
    if trip_distance_list[-1] < routebook.iloc[-1]["routebook_trip(m)"]:
        raise RouteMappingError("The RouteClass route is smaller than the route given in the routebook")

    trip_distance_list
    routebook_trip_distance_list = routebook["routebook_trip(m)"].tolist()
    trip_pointer = 0
    routebook_trip_pointer = 0
    data_index = [None] * len(trip_distance_list)

    while trip_pointer < len(trip_distance_list)-1 and routebook_trip_pointer < len(routebook_trip_distance_list):
        routebook_dist = routebook_trip_distance_list[routebook_trip_pointer]
        dist1 = abs(trip_distance_list[trip_pointer] - routebook_dist)
        dist2 = abs(trip_distance_list[trip_pointer+1] - routebook_dist)

        if dist1 < dist2:
            data_index[trip_pointer] = routebook_trip_pointer
            trip_pointer += 1
            routebook_trip_pointer += 1
        else:
            routebook_trip_pointer += 1

    if routebook_trip_pointer < len(routebook_trip_distance_list):
        data_index[-1] = routebook_trip_pointer
        routebook_trip_pointer += 1
    if routebook_trip_pointer != len(routebook_trip_distance_list):
        raise RouteMappingError("Unable to map the routebook data to the RouteClass route. Please ensure you have the correct route and is as accurate as possible")


    """
    4) Map the routebook data to the RouteClass route using the previously found routebook-to-RouteClass-route indices
    """
    







    return routebook




if __name__ == "__main__":
    pass
