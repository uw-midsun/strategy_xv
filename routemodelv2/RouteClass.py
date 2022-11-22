import pandas as pd




class RouteClass():


    def __init__(self, polyline_coordinates = None, interval_upper_bound = 100):
        """
        RouteClass is a wrapper intended to centralize and standardize the collection/storage of route-related data into 1 object
        @param polyline_coordinates: a polygonal chain representation of a route. It is of the form: a list of coordinate tuples
        @param interval_upper_bound: the distance upper bound for the distances between interpolated coordinates
        @return: RouteClass object
        """
        self.polyline_coordinates = polyline_coordinates
        self.interval_upper_bound = interval_upper_bound

        self._data = None


    def append_data(self, new_df: pd.DataFrame):
        """
        append_data is a method to append new columns (and associated data) into RouteClass's data/dataframe. Both dataframes
            require the same number of rows (of data). This method will automatically remove duplicated columns
        @param new_df: the dataframe for which you intend to add/merge the current pre-existing data to
        @return: None
        """
        if self._data is None:
            self._data = new_df

        else:
            if self._data.shape[0] != new_df.shape[0]:
                row_count = self._data.shape[0]
                raise TypeError(f"Both dataframes must have same number of rows when appending. RouteClass current has {row_count} rows of data")

            columns_to_merge = list(set(new_df.columns.tolist()) - set(self._data.columns.tolist()))
            df_to_merge = new_df[columns_to_merge]
            merged_df = pd.concat([self._data, df_to_merge], axis=1)
            self._data = merged_df


    def data(self):
        """
        data is a method to get the RouteClass's data (in a pandas dataframe)
        @param: None
        @return: pandas dataframe of RouteClass's data
        """
        if self._data is not None:
            return self._data


    def get_csv(self, filename = "data"):
        """
        get_csv is a method to save RouteClass's current data into a csv file
        @param filename: the name of the file that you want the csv to be saved as
        @return: None
        """
        if self._data is not None:
            data = self._data.fillna('')
            format_filename = f"{filename}.csv" if ".csv" not in filename else filename
            data.to_csv(format_filename)

