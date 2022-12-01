import requests
import json
import pandas as pd

# todo: add calculation of car elevation angle


def get_elevations(coordinates: list, BING_MAPS_API_KEY: str) -> pd.DataFrame:
    """
    get_elevations is a function that consumes a list of coordinates and bing maps API key and returns a pandas 
        dataframe containing the elevation of each coordinate and relative elevation gain (from to next coordinate)
    @param coordinates: a list of coordinate tuples
    @param BING_MAPS_API_KEY: your bing maps api key (as a string)
    @return pandas dataframe with data on coordinates, coordinates_elevations_data, relative_elevation_gains
    """


    """
    1) "Chunk" coordinates into lists of length 10000. Change list_len if there's an API size issue
    2) Compresses each coordinate chunk into 1 compressed query string for Bing Maps API
    - https://learn.microsoft.com/en-us/bingmaps/rest-services/elevations/point-compression-algorithm
    - Requires: coordinates
    - Result: compressed_coordinates_lst
    """
    list_len = 100
    split_coordinates = [coordinates[i:min(i+list_len, len(coordinates))] for i in range(0, len(coordinates), list_len)]
    compressed_coordinates_lst = []

    for coordinate_lst in split_coordinates:
        latitude = 0
        longitude = 0
        compressed_coordinates = ""

        for coordinate in coordinate_lst:
            newLatitude = round(coordinate[0] * 100000)
            newLongitude = round(coordinate[1] * 100000)

            dy = newLatitude - latitude
            dx = newLongitude - longitude
            latitude = newLatitude
            longitude = newLongitude

            dy = (dy << 1) ^ (dy >> 31)
            dx = (dx << 1) ^ (dx >> 31)

            index = int(((dy + dx) * (dy + dx + 1) / 2) + dy)
            while index > 0:
                rem = index & 31
                index = int((index - rem) / 32)
                if index > 0:
                    rem += 32
                compressed_coordinates += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"[rem]

        compressed_coordinates_lst.append(compressed_coordinates)


    """
    3) Requests the elevation for all the coordinates using our compressed coordinate query string and saves it into a list
    - Requires: compressed_coordinates_lst
    - Result: coordinates_elevations_data
    """
    coordinates_elevations_data = []
    for compressed_coordinates in compressed_coordinates_lst:
        API_query_string = f"http://dev.virtualearth.net/REST/v1/Elevation/List?points={compressed_coordinates}&heights=ellipsoid&key={BING_MAPS_API_KEY}"
        response = requests.post(API_query_string).json()

        if response["statusCode"] != 200:
            print("\n-> API Response\n", json.dumps(response, indent=2))
            raise ValueError(f"Bing Maps API request error {response['statusCode']}: {response['statusDescription']}")

        elevations_data = response["resourceSets"][0]["resources"][0]["elevations"]
        coordinates_elevations_data.extend(elevations_data)


    """
    4) Calculates the elevation change between the i and i+1 elevation in a list of elevations
    - Requires: coordinates_elevations_data
    - Result: relative_elevation_gains
    """
    relative_elevation_gains = []
    for i, elevation in enumerate(coordinates_elevations_data[:-1]):
        elevation1 = coordinates_elevations_data[i]
        elevation2 = coordinates_elevations_data[i+1]
        relative_elevation_gains.append(elevation2 - elevation1)
    relative_elevation_gains.append(None)


    """
    5) Build the coordinates, elevation, and relative_elevation_gains values in a dataframe for the user to use
    - Requires: coordinates
    - Requires: coordinates_elevations_data
    - Requires: relative_elevation_gains
    - Result: Dataframe
    """
    zip_coordinates = list(zip(*coordinates))
    latitude = zip_coordinates[0]
    longitude = zip_coordinates[1]

    df = pd.DataFrame({
            "latitude": latitude,
            "longitude": longitude,
            "elevation(m)": coordinates_elevations_data,
            "elevation_gains_to_next(m)": relative_elevation_gains,
        })
    return df




if __name__ == "__main__":
    pass

