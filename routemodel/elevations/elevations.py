from geopy import distance as calc_distance
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import warnings





class RouteElevation():
    def __init__(self, coordinates: list, BING_MAPS_API_KEY: str, sample_frequency_upper_bound: int = 1000, offset: int = 0, debug: bool = False):
        """
        Initializes a RouteElevation object which represents the elevations of the route with coordinates, coordinates. Builds 
        the elevation data and stores them
        @param coordinates: List of (lat, long) coordinate tuples which represents the route
        @param sample_frequency_upper_bound: Integer that represents the upper bound of the interval distance
        @param offset: Represents the x-axis offset of where to start counting for the resulting x-values
        @param debug: Set to True if want object to print data upon each step of the algorithm (for debugging purposes). Else, False
        @return: RouteElevation object
        """
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(message="This class is deprecated. Please use RouteModel paired with CoordinateElevations instead", category=DeprecationWarning)

        self._coordinates = coordinates
        self._number_of_segment_points = len(coordinates)
        self._sample_frequency_upper_bound = sample_frequency_upper_bound
        self._offset = offset
        self._debug = debug

        self._distance_between_coordinates = None
        self._sample_distances_between_coordinates = None
        self._query_coordinate_pairs = None
        self._elevation_data_between_coordinate_pairs = None
        self._x_axis_distance = None
        self._y_axis_elevations = None
        self._x_axis_segments = None
        self._y_axis_segments = None
        
        self.BING_MAPS_API_KEY = BING_MAPS_API_KEY
        self.build_elevations()



    def build_elevations(self):
        """
        Builds the elevation data and stores them in the class object. This method is ran upon object initialization.
        - Step-by-step process of what the algorithm is doing under the hood
        """
        self._distance_between_coordinates = self.build_distance_between_coordinates(self._coordinates)
        self._sample_distances_between_coordinates = self.build_sample_frequency_distances_between_coordinates(self._distance_between_coordinates, self._sample_frequency_upper_bound)
        self._query_coordinate_pairs = self.build_query_coordinate_pairs(self._coordinates)
        self._elevation_data_between_coordinate_pairs = self.build_elevation_data_between_coordinate_pairs(self._query_coordinate_pairs, self._sample_distances_between_coordinates)
        self._x_axis_distance = self.build_x_axis_distance(self._sample_distances_between_coordinates, self._offset)
        self._y_axis_elevations = self.build_y_axis_elevations(self._elevation_data_between_coordinate_pairs)
        self._x_axis_segments = self.build_x_axis_segments(self._x_axis_distance, self._sample_distances_between_coordinates)
        self._y_axis_segments = self.build_y_axis_segments(self._y_axis_elevations, self._sample_distances_between_coordinates)



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
            distance = round(calc_distance.distance(coordinates[i-1], coordinates[i]).m, 2)
            distance_between_coordinates.append(distance)

        if self._debug == True:
            print("\n-> Distance between coordinates\n", distance_between_coordinates)

        return distance_between_coordinates



    def build_sample_frequency_distances_between_coordinates(self, distance_between_coordinates: list, sample_frequency_upper_bound: int = 1000):
        """
        Determines the amount of points/intervals as well as the interval distance to use when determining the polyline elevation(s) between 2 coordinates
            - The max number of intervals sampled between 2 points is 1023, which may result in the point intervals exceeding the sample_frequency_upper_bound
            - To get around this issue, use multiple lines/segments to represent 1 larger segment so that the total max number of intervals is 1023*num_of_segments
        @param distance_between_coordinates: List of n-1 length where the i-th entry represents the distance between coordinate/point n and n+1
        @param sample_frequency_upper_bound: Integer that represents the upper bound of the interval distance
        @return: List of tuples where the tuple[0] represents the number of points used (tuple[0]-1 represents the number of intervals) and tuple[1] represents
            the interval distance (distance between polyline points). The i-th element/tuple in the list represents the data for between coordinates n and n+1
        """
        sample_distances_between_coordinates = [] 
        for distance in distance_between_coordinates:
            sample_point_frequency = int(distance//sample_frequency_upper_bound + 2)
            sampling_distance = round(distance/(sample_point_frequency - 1), 2)
            if sample_point_frequency > 1024:
                sample_point_frequency = 1024
                sampling_distance = round(distance/1023, 2)

            sample_distances_between_coordinates.append((sample_point_frequency, sampling_distance))

        if self._debug == True:
            print("\n-> Sample distances between coordinates\n", sample_distances_between_coordinates)

        return sample_distances_between_coordinates



    def build_query_coordinate_pairs(self, coordinates: list):
        """
        Builds the coordinates query string between 2 adjacent coordinate pairs, which will then be used in the API request
        @param coordinates: list of (lat, long) coordinate tuples
        @return: A list of query string for each adjacent coordinate pair
        """
        if len(coordinates) < 2:
            raise ValueError("'build_query_coordinate_pairs' function requires at least 2 coordinates")

        query_coordinate_pairs = []
        for i, coordinate in enumerate(coordinates[1:], start=1):
            query_string = f"{coordinates[i-1][0]},{coordinates[i-1][1]},{coordinates[i][0]},{coordinates[i][1]}"
            query_coordinate_pairs.append(query_string)
            # print([coordinates[i-1], coordinates[i]])

        if self._debug == True:
            print("\n-> Query coordinate pairs\n", query_coordinate_pairs)

        return query_coordinate_pairs



    def build_elevation_data_between_coordinate_pairs(self, queried_coordinate_pairs: list, sample_frequency_distances_between_coordinates: list):
        """
        Requests the elevation between 2 adjacent coordinates using the desired number of intervals between the 2 coordinates
        @param queried_coordinate_pairs: A list of query string for each adjacent coordinate pair
        @param sample_frequency_distances_between_coordinates: List of tuples where the tuple[0] represents the number of points used (tuple[0]-1 represents 
            the number of intervals) and tuple[1] represents the interval distance (distance between polyline points). The i-th element/tuple in the list 
            represents the data for between coordinates n and n+1
        @return: Returns a list of lists, where the "inner" lists represent the elevations between 2 adjacent 
            coordinates using the desired number of intervals between the said coordinates. The i-th entry represents the elevations between 
            coordinate[i] and coordinate[i+1]
        """
        BING_MAPS_API_KEY = self.BING_MAPS_API_KEY

        elevation_data_between_coordinate_pairs = []
        for i, queried_coordinate_pair in enumerate(queried_coordinate_pairs):
            sample_frequency = sample_frequency_distances_between_coordinates[i][0]
            API_query_string = f"http://dev.virtualearth.net/REST/v1/Elevation/Polyline?points={queried_coordinate_pair}&heights=ellipsoid&samples={sample_frequency}&key={BING_MAPS_API_KEY}"
            response = requests.post(API_query_string).json()

            if response["statusCode"] != 200:
                print("\n-> API Response\n", json.dumps(response, indent=2))
                raise ValueError(f"Bing Maps API request error {response['statusCode']}: {response['statusDescription']}")

            elevations = response["resourceSets"][0]["resources"][0]["elevations"]
            elevation_data_between_coordinate_pairs.append(elevations)

        if self._debug == True:
            print("\n-> Elevation data between coordinate pairs\n", elevation_data_between_coordinate_pairs)

        return elevation_data_between_coordinate_pairs



    def build_x_axis_distance(self, sample_frequency_distances_between_coordinates: list, offset: int = 0):
        """
        Builds the x-values that represents the distance 
        @param sample_frequency_distances_between_coordinates: List of tuples where the tuple[0] represents the number of points used (tuple[0]-1 represents 
            the number of intervals) and tuple[1] represents the interval distance (distance between polyline points). The i-th element/tuple in the list 
            represents the data for between coordinates n and n+1
        @param offset: represents the x-axis offset of where to start counting for the resulting x-values
        @return: List of numbers that represents the x-values that are to be plotted/used
        """
        x_axis_distance = [offset]
        accumulated_distance = offset
        for distances_between_coordinates in sample_frequency_distances_between_coordinates:
            intervals = distances_between_coordinates[0] - 1
            interval_distance = distances_between_coordinates[1]
            for i in range(intervals):
                accumulated_distance += interval_distance
                x_axis_distance.append(int(accumulated_distance))

        if self._debug == True:
            print("\n-> X-axis distance\n", x_axis_distance)

        return(x_axis_distance)



    def build_y_axis_elevations(self, elevation_data_between_coordinate_pairs: list):
        """
        Builds the y-values that represents the elevations 
        @param elevation_data_between_coordinate_pairs: Returns a list of lists, where the "inner" lists represent the elevations between 2 adjacent 
            coordinates using the desired number of intervals between the said coordinates. The i-th entry represents the elevations between 
            coordinate[i] and coordinate[i+1]
        @return: List of numbers that represents the y-values that are to be plotted/used
        """
        y_axis_elevations = []
        for i, elevations in enumerate(elevation_data_between_coordinate_pairs):
            if i == 0:
                y_axis_elevations +=  elevations
            else:
                y_axis_elevations += elevations[1:]

        if self._debug == True:
            print("\n-> Y-axis elevations\n", y_axis_elevations)

        return y_axis_elevations



    def build_x_axis_segments(self, x_axis_distance: list, sample_frequency_distances_between_coordinates: list):
        """
        Builds the x-values that represents the coordinate points/segments (distance)
        @param x_axis_distance: List of numbers that represents the x-values that are to be plotted/used
        @param sample_frequency_distances_between_coordinates: List of tuples where the tuple[0] represents the number of points used (tuple[0]-1 represents 
            the number of intervals) and tuple[1] represents the interval distance (distance between polyline points). The i-th element/tuple in the list 
            represents the data for between coordinates n and n+1
        @return: List that represents the x-values of the coordinate points/segments (distance) that are to be plotted/used
        """
        idx = 0
        x_axis_segments = [x_axis_distance[0]]
        for i, distance in enumerate(sample_frequency_distances_between_coordinates): 
            idx += distance[0] - 1
            x_axis_segments.append(x_axis_distance[idx])

        if self._debug == True:
            print("\n-> X-axis segments\n", x_axis_segments)

        return x_axis_segments


        
    def build_y_axis_segments(self, y_axis_elevations: list, sample_frequency_distances_between_coordinates: list):
        """
        Builds the y-values that represents the coordinate points/segments (elevations)
        @param y_axis_elevations: List of numbers that represents the y-values that are to be plotted/used
        @param sample_frequency_distances_between_coordinates: List of tuples where the tuple[0] represents the number of points used (tuple[0]-1 represents 
            the number of intervals) and tuple[1] represents the interval distance (distance between polyline points). The i-th element/tuple in the list 
            represents the data for between coordinates n and n+1
        @return: List that represents the y-values of the coordinate points/segments (elevations) that are to be plotted/used
        """
        idx = 0
        y_axis_segments = [y_axis_elevations[0]]
        for i, elevations in enumerate(sample_frequency_distances_between_coordinates): 
            idx += elevations[0] - 1
            y_axis_segments.append(y_axis_elevations[idx])

        if self._debug == True:
            print("\n-> Y-axis segments\n", y_axis_segments)

        return y_axis_segments
        


    def get_elevations(self, start_point: int = None, end_point: int = None):
        """
        Builds the distance and elevation values for the user to use
            - If both params are None, returns all the distances and elevations for all the coordinates
        @param start_point (optional): The starting coordinate to start getting elevations from
        @param end_point (optional): The ending coordinate to stop getting elevations from
        @return: List of numbers that represents the x-values (distances) from start_point to end_point
        @return:List of numbers that represents the y-values (elevations) from start_point to end_point
        """
        sample_distances_between_coordinates = self._sample_distances_between_coordinates
        x_axis_distance = self._x_axis_distance
        y_axis_elevations = self._y_axis_elevations
        points = [*filter(lambda point: point is not None, [start_point, end_point])]

        if (len(points) != 0 and len(points) != 2):
            raise ValueError("get_elevations requires 0 or 2 parameters: start_point and end_point (0-indexed)")

        if len(points) == 0:
            return x_axis_distance, y_axis_elevations

        if len(points) == 2:
            assert 0 <= start_point, "start_point must be greater than or equal to 0"
            assert end_point <= self._number_of_segment_points - 1, f"end_point must be less than {self._number_of_segment_points}"
            assert start_point < end_point, "start_point must be less than end_point"
            start_point, end_point = points

            end_index = -1 * end_point
            for i in range(end_point):
                end_index += sample_distances_between_coordinates[i][0]

            start_index = -1 * start_point
            for i in range(start_point):
                start_index += sample_distances_between_coordinates[i][0]

            return x_axis_distance[start_index:end_index+1], y_axis_elevations[start_index:end_index+1]



    def get_dataframe(self, start_point: int = None, end_point: int = None):
        """
        Builds the distance and elevation values in a dataframe for the user to use
            - If both params are None, returns a dataframe with all the distances and elevations
        @param start_point (optional): The starting coordinate to start getting elevations from
        @param end_point (optional): The ending coordinate to stop getting elevations from
        @return: dataframe where each row represents the distance and its associated elevation
        """
        distances, elevations = self.get_elevations(start_point, end_point)
        return pd.DataFrame({
            "distance": distances,
            "elevation": elevations
        })
                


    def plot_elevations(self, start_point: int = None, end_point: int = None):
        """
        Plots the distance and elevation values for the user
            - If both params are None, plots all the distances and elevations for all the coordinates
        @param start_point (optional): The starting coordinate to start plotting elevations from
        @param end_point (optional): The ending coordinate to stop plotting elevations from
        """
        points = [*filter(lambda point: point is not None, [start_point, end_point])]

        if (len(points) != 0 and len(points) != 2):
            raise ValueError("plot_elevations requires 0 or 2 parameters: start_point and end_point (0-indexed)")

        else:
            x_axis_distance, y_axis_elevations = self.get_elevations(start_point, end_point)
            start_index, end_index = start_point or 0, end_point or self._number_of_segment_points - 1
            x_axis_segments, y_axis_segments = self._x_axis_segments[start_index:end_index+1], self._y_axis_segments[start_index:end_index+1]

            fig, ax = plt.subplots()
            ax.plot(x_axis_distance, y_axis_elevations, zorder=1)
            ax.scatter(x_axis_segments, y_axis_segments, color="red", marker=".", zorder=2)
            for i in range(start_index, end_index+1):
                ax.annotate(i, (x_axis_segments[i-start_index], y_axis_segments[i-start_index]), horizontalalignment="center")
            ax.set_title(f"Route Elevation from point {start_index} to {end_index} ({len(x_axis_distance)} datapoints)")
            ax.set_xlabel("Distance (m)")
            ax.set_ylabel("Elevation (m)")
            # fig.savefig('elevations.png', bbox_inches='tight')
            plt.show()





class CoordinateElevation():
    def __init__(self, coordinates: list, BING_MAPS_API_KEY: str, debug: bool = False):
        """
        Initializes a CoordinateElevation object which represents the elevations of each coordinate in coordinates. Builds 
        the elevation data and stores them
        @param coordinates: List of (lat, long) coordinate tuples which represents the route
        @param debug: Set to True if want object to print data upon each step of the algorithm (for debugging purposes). Else, False
        @return: CoordinateElevation object
        """
        self._coordinates = coordinates
        self._number_of_coordinates = len(coordinates)

        self._debug = debug
        self._compressed_coordinates_lst = None
        self._elevation_data = None

        self.BING_MAPS_API_KEY = BING_MAPS_API_KEY
        self.build_elevations()



    def build_elevations(self):
        """
        Builds the elevation data and stores them in the class object. This method is ran upon object initialization.
        - Step-by-step process of what the algorithm is doing under the hood
        """
        self._compressed_coordinates_lst = self.compress_coordinates(self._coordinates)
        self._elevation_data = self.build_elevation_data(self._compressed_coordinates_lst)



    def compress_coordinates(self, coordinates: list):
        """
        Compresses all the coordinates into 1 compressed query string for Bing Maps API. This allows for 1 single API call
            - https://learn.microsoft.com/en-us/bingmaps/rest-services/elevations/point-compression-algorithm
        @param coordinates: List of (lat, long) coordinate tuples which represents the route
        @return: Compressed query string that represents all the coordinates
        """
        split_coordinates = [coordinates[i:i+10000] for i in range(0, len(coordinates), 10000)] # Limit 10000 coordinates per request. Change limit if there's an API size issue
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

            if self._debug == True:
                print("\n-> Compressed Coordinates\n", compressed_coordinates)
            compressed_coordinates_lst.append(compressed_coordinates)

        return compressed_coordinates_lst



    def build_elevation_data(self, compressed_coordinates_lst: str):
        """
        Requests the elevation for all the coordinates using our compressed coordinate query string
        @param compressed_coordinates: Compressed query string that represents all the coordinates
        @return: Returns a list of integers, where the i-th entry represents the elevation for the i-th coordinates
        """
        BING_MAPS_API_KEY = self.BING_MAPS_API_KEY
        coordinates_elevations_data = []
        for compressed_coordinates in compressed_coordinates_lst: # Limit 10000 coordinates per request (See compress_coordinates method)
            API_query_string = f"http://dev.virtualearth.net/REST/v1/Elevation/List?points={compressed_coordinates}&heights=ellipsoid&key={BING_MAPS_API_KEY}"
            response = requests.post(API_query_string).json()

            if response["statusCode"] != 200:
                print("\n-> API Response\n", json.dumps(response, indent=2))
                raise ValueError(f"Bing Maps API request error {response['statusCode']}: {response['statusDescription']}")

            elevations_data = response["resourceSets"][0]["resources"][0]["elevations"]
            zoom_level = response["resourceSets"][0]["resources"][0]["zoomLevel"]

            if self._debug == True:
                print("\n-> Elevation data each each coordinate\n", elevations_data)
                print("\n-> Zoom Level\n", zoom_level)
            coordinates_elevations_data.extend(elevations_data)

        return coordinates_elevations_data



    def get_elevations(self, start_point: int = None, end_point: int = None):
        """
        Builds the coordinate and elevation values for the user to use
            - If both params are None, returns all the distances and elevations for all the coordinates
        @param start_point (optional): The starting coordinate index to start getting elevations from
        @param end_point (optional): The ending coordinate index to stop getting elevations from
        @return: List of coordinates from start_point to end_point
        @return: List of numbers that represents coordinate elevations from start_point to end_point
        """
        coordinates = self._coordinates
        elevation_data = self._elevation_data
        points = [*filter(lambda point: point is not None, [start_point, end_point])]

        if (len(points) != 0 and len(points) != 2):
            raise ValueError("get_elevations requires 0 or 2 parameters: start_point and end_point (0-indexed)")

        if len(points) == 0:
            return coordinates, elevation_data

        if len(points) == 2:
            assert 0 <= start_point, "start_point must be greater than or equal to 0"
            assert end_point <= self._number_of_coordinates - 1, f"end_point must be less than {self._number_of_coordinates}"
            assert start_point < end_point, "start_point must be less than end_point"
            start_point, end_point = points

            return coordinates[start_point:end_point+1], elevation_data[start_point:end_point+1]



    def get_dataframe(self, start_point: int = None, end_point: int = None):
        """
        Builds the coordinates and elevation values in a dataframe for the user to use
            - If both params are None, returns a dataframe with all the coordinates and elevations
        @param start_point (optional): The starting coordinate index to start getting elevations from
        @param end_point (optional): The ending coordinate index to stop getting elevations from
        @return: dataframe where each row represents the coordinate and its associated elevation
        """
        coordinates, elevations = self.get_elevations(start_point, end_point)
        zip_coordinates = list(zip(*coordinates))
        latitude = zip_coordinates[0]
        longitude = zip_coordinates[1]

        return pd.DataFrame({
            "latitude": latitude,
            "longitude": longitude,
            "elevation":elevations
        })



    def plot_elevations(self, start_point: int = None, end_point: int = None):
        """
        Plots the coordinate index and elevation values for the user
            - If both params are None, plots all the distances and elevations for all the coordinates
        @param start_point (optional): The starting coordinate index to start getting elevations from
        @param end_point (optional): The ending coordinate index to stop getting elevations from
        """
        coordinates, elevations = self.get_elevations(start_point, end_point)
        fig, ax = plt.subplots()
        ax.plot(elevations)
        ax.set_title(f"Route Elevation from point {start_point} to {end_point} ({len(elevations)} datapoints)")
        ax.set_ylabel("Elevation (m)")
        ax.set_xlabel("Coordinate Index")
        ax.set_xticks([])
        # ax.set_xticks(range(len(elevations)))
        # fig.savefig('elevations.png', bbox_inches='tight')
        plt.show()





if __name__ == "__main__":
    pass
