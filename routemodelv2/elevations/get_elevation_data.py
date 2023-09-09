import requests
import json
import pandas as pd
from pandas import json_normalize

# Dataset Used: {srtm30m} https://www.opentopodata.org/datasets/srtm/
# Params: dataset, location <lat,long>
# Return: Information returned as a json object [Elevation is in metres above sea level]

#  STEPS:
#  Read the CSV
#  Create a list of values that are valid to pass through the request
#          Combine lat & long into a single coordinate with no parentheses/quotations
#  Turn column of coordinates into a list
#  Loop through the list of coordinates, add corresponding elevation to elevation_data
#  Create a new column in CSV that holds elevation_data
#  Export as a new CSV

sample_coordinates_df = pd.read_csv("sample_coordinates.csv")
parameters_list = pd.series(sample_coordinates_df.apply(lambda row: ','.join([str(row['latitude']), str(row['longitude'])]), axis=1))

elevation_data = []
for item in parameters_list:
    try:
        response = requests.get(('https://api.opentopodata.org/v1/srtm30m?locations={}&&interpolation=bilinear'.format(item)))
        response.raise_for_status()
        data = response.json()
        elevation_value=(data['results'][0]['elevation'])
        elevation_data.append(elevation_value)
    except Exception as e:
        print(f"Unexpected error encountered at {item}: ", e)

sample_coordinates_df['elevation']=elevation_data
sample_coordinates_df.to_csv('appended_elevation_data.csv', index=False)

