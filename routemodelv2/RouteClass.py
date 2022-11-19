import pandas as pd




class RouteClass():


    def __init__(self, polyline_coordinates = None, interval_upper_bound = 100):
        self.polyline_coordinates = polyline_coordinates
        self.interval_upper_bound = interval_upper_bound

        self._data = None


    def append_data(self, new_df: pd.DataFrame):
        if self._data is None:
            self._data = new_df

        else:
            if self._data.shape[0] != new_df.shape[0]:
                raise TypeError("Both dataframes must have same number of rows when appending")

            columns_to_merge = list(set(new_df.columns.tolist()) - set(self._data.columns.tolist()))
            df_to_merge = new_df[columns_to_merge]
            merged_df = pd.concat([self._data, df_to_merge], axis=1)
            self._data = merged_df


    def data(self):
        if self._data is not None:
            return self._data


    def get_csv(self, filename = "data"):
        if self._data is not None:
            data = self._data.fillna('')
            format_filename = f"{filename}.csv" if ".csv" not in filename else filename
            data.to_csv(format_filename)

