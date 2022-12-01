import os
import numpy as np
import pandas as pd
import warnings




class RouteMappingError(Exception):
    pass


def map_routebook_data(trip_distance_list, routebook_filepath, bypass_dist_error = False):
    """
    map_routebook_data
    @param trip_distance_list: list of trip distance at each coordinate (from RouteClass)
    @param routebook_filepath: The filepath of the routebook csv
    @param bypass_dist_error: Bypasses the error exception when the routebook trip distance > RouteClass trip distance
    @return: dataframe of the routebook data that has been mapped/scaled to our routebook dataframe
    """


    """
    1) Get routebook data and clean/remove empty strings
    """
    routebook = pd.read_csv(routebook_filepath)
    routebook.columns = routebook.columns.str.replace(' ', '')
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
    total_trip_dist = trip_distance_list[-1]
    total_routebook_dist = routebook.iloc[-1]["routebook_trip(m)"]
    warnings.warn(f"There is a {abs(total_trip_dist - total_routebook_dist)}m distance discrepancy between the routebook and RouteClass routes\n")

    if total_trip_dist < total_routebook_dist and not bypass_dist_error:
        raise RouteMappingError("The RouteClass route is smaller than the route given in the routebook")

    trip_distance_list
    routebook_trip_distance_list = routebook["routebook_trip(m)"].tolist()
    trip_pointer = 0
    routebook_trip_pointer = 0
    indexed_route_data = [None] * len(trip_distance_list)

    while trip_pointer < len(trip_distance_list)-1 and routebook_trip_pointer < len(routebook_trip_distance_list):
        routebook_dist = routebook_trip_distance_list[routebook_trip_pointer]
        dist1 = abs(trip_distance_list[trip_pointer] - routebook_dist)
        dist2 = abs(trip_distance_list[trip_pointer+1] - routebook_dist)

        if dist1 < dist2:
            indexed_route_data[trip_pointer] = routebook_trip_pointer
            trip_pointer += 1
            routebook_trip_pointer += 1
        else:
            trip_pointer += 1

    if routebook_trip_pointer < len(routebook_trip_distance_list):
        indexed_route_data[-1] = routebook_trip_pointer
        routebook_trip_pointer += 1

    if routebook_trip_pointer != len(routebook_trip_distance_list):
        raise RouteMappingError("Unable to map the routebook data to the RouteClass route. Please ensure you have the correct route and is as accurate as possible")


    """
    4) Map routebook data to the RouteClass route using previously found routebook-to-RouteClass-route indices then create the mapped/scaled routebook dataframe
    """
    column_names = routebook.columns.values

    for i, data_index in enumerate(indexed_route_data):
        if data_index is not None:
            routebook_row = routebook.iloc[data_index].tolist()
            indexed_route_data[i] = routebook_row
        else:
            empty_row = [np.nan] * len(column_names)
            indexed_route_data[i] = empty_row
            
    mapped_routebook_data = pd.DataFrame(columns=column_names, data=indexed_route_data)
    mapped_routebook_data["trip(m)"] = trip_distance_list


    return mapped_routebook_data.fillna('')




if __name__ == "__main__":
    pass
