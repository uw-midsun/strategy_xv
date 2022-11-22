## `Route.py` and `RouteClass.py` documentation

`RouteClass` is a wrapper inteaded to store/collect route-related data as a single object. It abstracts all the functions that are used to get/calculate the data. 

1. Start by familarizing yourself with `RouteClass.py`
2. Look at `route.py` as an example on how to use `RouteClass`
3. Use `route.py` as a sandbox for your development

## How to use `RouteClass` in `route.py`

1. Get whatever data you need from `RouteClass` using the `.data()` method
2. Using your collected data, use it as the input for your function(s)
3. Your functions are expected to return a Pandas Dataframe
4. Merge your Pandas Dataframe into `RouteModel` using the `.append_data()` method. Your Dataframe must have the same number of rows as the Dataframe from `RouteClass.data()`
5. Repeat this dev process
6. Save `RouteClass`'s data into a csv file using the `get_csv()` method from `RouteClass`