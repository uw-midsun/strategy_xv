import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
from geopy.distance import distance as geodist

class ETAQuery():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.route_model = pd.read_csv(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/route_model_db.csv')))
        self.checkpoint_model = pd.read_csv(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/checkpoint_model_db.csv')))
        self.checkpoint_coords = self.checkpoint_model.loc[:, ['latitude', 'longitude']].values.tolist()
        self.ckpt_to_route_model_index = self.checkpoint_model.loc[:, ['route_model_index']].values.tolist()
        self.eta_to_checkpoint = []
        self.speed = self.get_speed_at_point(lat, lon) # Speed in km/h

        self.generate_eta()

    def get_speed_at_point(self, lat, lon):
        return 5 # TODO: Take speed from route model after it is precomputed

    def find_closest_point(self, lat, lon):
        '''
        The function takes in a coordinate point (lat/lon) and finds the closest point to it inside the route model 
        @param lat: float representing the latitude
        @param lon: float representing the longitude
        @return: a row of the route_model dataframe containing information about the closest point on the race route
        '''

        distances = self.route_model.apply(lambda row: geodist((lat, lon), (row['latitude'], row['longitude'])).meters, axis=1)
        return self.route_model.iloc[distances.idxmin()]
        
    def generate_eta(self):
        """
        @return: a list of float values representing the time it takes to reach the checkpoints
        """
        closest_point = self.find_closest_point(self.lat, self.lon)
        current_checkpoint = closest_point['checkpoint']
        next_closest_checkpoint = current_checkpoint+1
        
        n = len(self.checkpoint_coords)
        eta = [-1 for _ in range(n)]

        if next_closest_checkpoint >= n: 
            self.eta = eta
            return self.eta

        slat = self.lat
        slon = self.lon
        elat = self.checkpoint_coords[next_closest_checkpoint][0]
        elon = self.checkpoint_coords[next_closest_checkpoint][1]

        dist_to_next_checkpoint = geodist((slat, slon), (elat, elon)).meters
        # Unit conversion is to put meters into kilometers and time into minutes
        eta[next_closest_checkpoint] =  (dist_to_next_checkpoint/1000) / self.speed * 60 

        for future_checkpoint in range(next_closest_checkpoint+1, n):
            a = self.ckpt_to_route_model_index[next_closest_checkpoint]
            b = self.ckpt_to_route_model_index[future_checkpoint]

            print(self.route_model.iloc[b]['trip(m)'])

            # Unit conversion is to put meters into kilometers and time into minutes
            eta_next_to_future = ((self.route_model.iloc[b]['trip(m)'] - self.route_model.iloc[a]['trip(m)'])/1000) / self.speed * 60
            eta[future_checkpoint] = eta[next_closest_checkpoint] + eta_next_to_future

        self.eta = eta
        return eta


    def get_times(self):
        """
        @return: a list of float values representing the time it takes to reach the checkpoints
        """
        return self.eta
    
    def get_time_to_point(self, lat, lon):
        """
        @return: float representing the time it takes to reach a given point
        """
        closest_point = self.find_closest_point(lat, lon)
        return self.eta[closest_point['checkpoint']]