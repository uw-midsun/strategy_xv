import os
import pandas as pd

"""
This etl script creates a checkpoint csv and modfiies the route model csv to include a checkpoint column
"""

def generate_checkpoints(route_model, freq):
    """
    Generates 'checkpoints' which are {freq} meters apart where weather and other API calls can be made from
    @param freq: the distance in meters between each generated checkpoint
    @return: List of coordinates representing each of the checkpoints
    """
    checkpoint_coords = [] 
    checkpoint = [] # Stores the index of the last checkpoint passed for any given route model point

    lst_checkpoint = -1

    for index, row in route_model.iterrows():
        cur_checkpoint = int(row['trip(m)'] // freq)
        if cur_checkpoint != lst_checkpoint: 
            checkpoint_coords.append([row['latitude'], row['longitude'], index])
        checkpoint.append(cur_checkpoint)
        lst_checkpoint = cur_checkpoint

    route_model['checkpoint'] = checkpoint

    checkpoint_model = pd.DataFrame(checkpoint_coords, columns=["latitude", "longitude", "route_model_index"])
    checkpoint_model['last_updated'] = float('nan')
    checkpoint_model['forecast_time'] = float('nan')

    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    checkpoint_model.to_csv(os.path.normpath(os.path.join(dir_path, '../data/checkpoint_model_db.csv')), index=False) # Checkpoint database
    route_model.to_csv(os.path.normpath(os.path.join(dir_path, '../data/route_model_db.csv')), index=False) # Route database


DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ROUTE_MODEL_PATH = os.path.normpath(os.path.join(DIR_PATH, '../data/route_model_db.csv'))
CHECKPOINT_FREQ = 1000 # meters

route_model = pd.read_csv(ROUTE_MODEL_PATH)
generate_checkpoints(route_model, CHECKPOINT_FREQ)