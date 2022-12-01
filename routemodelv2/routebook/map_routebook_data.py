import os
import numpy as np
import pandas as pd




class TripDistanceError(Exception):
    pass

def map_routebook_data(trip_distance_list, routebook_filepath):
    routebook = pd.read_csv(routebook_filepath)
    routebook.replace(r'^\s*$', np.nan, regex=True, inplace = True)

    # Reformat + rename columns and convert values to SI units
    del routebook['Int']
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
    routebook['routebook_trip(m)'] = routebook['routebook_trip(m)'].apply(lambda x: x*1609.344) # miles to meters
    routebook['speed_limit(m/s)'] = routebook['speed_limit(m/s)'].map(float).apply(lambda x: x*0.44704) # mph to m/s

    # if trip_distance_list[-1] < routebook.iloc[-1]['routebook_trip(m)']:
    #     raise TripDistanceError('The selected route is smaller than the route given in the routebook')

    trip_distance_list
    routebook_trip_distance_list = routebook['routebook_trip(m)'].tolist()

    routebook_data_index = [None] * len(trip_distance_list)

    trip_pointer = 0
    routebook_trip_pointer = 0

    # while 



    return routebook




if __name__ == "__main__":
    pass
