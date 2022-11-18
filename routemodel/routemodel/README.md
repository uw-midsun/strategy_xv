# RouteModel

**Prerequisite: Read the [RouteElevation documentation](https://github.com/uw-midsun/strategy_xv/tree/main/routemodel/elevations) first to understand what a polygonal chain is and how it's used to represent a route** 

---
## Introduction
RouteModel is a model that consumes a polygonal chain representation of a route and returns an interpolated route 

---
## User Guide
When using this, there are only 4 things that you need to know:

- The object initialization
- The `get_data()` method
- The `get_csv()` method
- Dataframe values
- The `get_elevations_list()` method

### The object initialization
Initializing the object requires 2 required parameters, `coordinate_lst_input`: a polygonal chain representation of the route, and `interval_upper_bound`: an uppper bound for the distance between coordinates

### The `get_data()` method
Returns a pandas dataframe of the interpolated route

### The `get_csv()` method
Consumes a string, `filename`, and saves a csv of the interpolated route as `<filename>.csv` in current directory

### Dataframe fields
- `polyline_point_index`: The polygonal chain point index of the coordinate,
- `latitude`: Latitude,
- `longitude`: Longitude,
- `trip_meters`: Cumulative number of meters completed (at this point relative to the start of the route),
- `dist_to_next_coordinate`: Distance to next coordinate (in meters)
- `true_bearing_to_next`: True north bearing to next coordinate
- `bearing_to_next_360`: True north bearing to next coordinate in 360 degrees
- `true_bearing_to_prev`: True north bearing to previous coordinate
- `bearing_to_prev_360`: True north bearing to previous coordinate in 360 degrees
- `general_travel_direction`: General direction of car at current coordinate
- `turn_bearing`: Relative turn bearing for car at current coordinate
- `turn_type`: Type of turn for the car
- `relative_turn_angle`: Formatted relative turn angle for car at current coordinate

### The `get_elevations_list()` method
Returns a list of tuples, where each tuple represents a (latitude, longitude) coordinate of the interpolated route

---
## Sample code (Dataframe fields may be outdated in the example; refer to the `Dataframe fields` section for latest)

```
### CODE ###

coordinate_lst_input = [
        (43.81857948416717, -79.40101625627213), 
        (43.82045746557804, -79.3901457521166), 
        (43.81990512423598, -79.38545051088512)
        ]
interval_upper_bound = 100

route = RouteModel(coordinate_lst_input, interval_upper_bound) 
print(route.get_data())


### PRINTED VALUES ###

   polyline_point_index   latitude  longitude dist_to_next_coordinate true_bearing_to_next bearing_to_next_360 true_bearing_to_prev bearing_to_prev_360 general_travel_direction turn_bearing     turn_type relative_turn_angle
0                   0.0  43.818579 -79.401016               99.896547            76.576401           76.576401                                                             N77°E
1                        43.818788 -79.399808               99.896547            76.577237           76.577237          -103.422763          256.577237                    N77°E     0.000836
2                        43.818997 -79.398601               99.896547            76.578073           76.578073          -103.421927          256.578073                    N77°E     0.000836
3                        43.819206 -79.397393               99.896547             76.57891            76.57891           -103.42109           256.57891                    N77°E     0.000836
4                        43.819414 -79.396185               99.896547            76.579746           76.579746          -103.420254          256.579746                    N77°E     0.000836
5                        43.819623 -79.394977               99.896547            76.580582           76.580582          -103.419418          256.580582                    N77°E     0.000836
6                        43.819832 -79.393769               99.896547            76.581419           76.581419          -103.418581          256.581419                    N77°E     0.000836
7                        43.820040 -79.392561               99.896547            76.582255           76.582255          -103.417745          256.582255                    N77°E     0.000836
8                        43.820249 -79.391354               99.896547            76.583091           76.583091          -103.416909          256.583091                    N77°E     0.000836
9                   1.0  43.820457 -79.390146               95.668988            99.226778           99.226778          -103.416072          256.583928                     S9°E    22.643687  Slight Right           22.643687
10                       43.820319 -79.388972               95.668988            99.227591           99.227591           -80.772409          279.227591                     S9°E     0.000813
11                       43.820181 -79.387798               95.668988            99.228404           99.228404           -80.771596          279.228404                     S9°E     0.000813
12                       43.820043 -79.386624               95.668988            99.229217           99.229217           -80.770783          279.229217                     S9°E     0.000813
13                  2.0  43.819905 -79.385451                                                                            -80.769971          279.230029
```
