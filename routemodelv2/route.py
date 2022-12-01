import os
import dotenv
import numpy as np
import pandas as pd

from RouteClass import RouteClass
from coordinates.get_coordinates import get_coordinates
from elevations.get_elevations import get_elevations
from routebook.map_routebook_data import map_routebook_data
import time
t0 = time.time()
t1 = time.time()

"""
API KEYS
"""
dotenv.load_dotenv()
# BING_MAPS_API_KEY = "" # Manual option
BING_MAPS_API_KEY = os.getenv("BING_MAPS_API_KEY")


"""
Step 1: Initiate RouteClass wrapper for our route
"""
polyline_coordinates = [
    (43.467879339595996, -80.56616840836313),
    (43.47883157462026, -80.53538493288134),
    (43.473830662244815, -80.53170344584917),
    (43.471525236984746, -80.53744468397863),
    (43.4644417537584, -80.54157837541729),
    (43.46348360838345, -80.53993555488016),
    (43.46266401802443, -80.53908339764159)
    ]
polyline_coordinates_2022_B_Loop = [
    (40.8829378816515, -98.37406855532743),
    (40.88303262290332, -98.37402201117517),
    (40.882921640280436, -98.37347780262579),
    (40.88294870923001, -98.3729550759928),
    (40.883056984922696, -98.37254691950501),
    (40.88323834630254, -98.37222469075867),
    (40.88354422332468, -98.37191320297053),
    (40.88393671833501, -98.37168048219625),
    (40.884356279374096, -98.37165900027982),
    (40.88480561276309, -98.37186665880527),
    (40.885187273075935, -98.37230703812195),
    (40.88531719948494, -98.37257556207723),
    (40.885379455798876, -98.37281902379671),
    (40.88545253922308, -98.37316631477889),
    (40.88646757846244, -98.3731484132071),
    (40.887044113825155, -98.3730266823367),
    (40.88793732767246, -98.37301594137848),
    (40.887888607228646, -98.36852622070076),
    (40.887542149696934, -98.35897750849163),
    (40.887275916856474, -98.3397462910507),
    (40.858084895499736, -98.33990940157038),
    (40.82569092682914, -98.34058548005243),
    (40.77376804238631, -98.34005464594843),
    (40.772412410380845, -98.34062793999414),
    (40.771898503369655, -98.34121293391789),
    (40.77143775583309, -98.34204362529023),
    (40.7710744718689, -98.34309661435378),
    (40.77098586572269, -98.34404430451097),
    (40.771010164750734, -98.3782267398604),
    (40.820256453345706, -98.37835518348754),
    (40.88797476498994, -98.37820199597991),
    (40.88788783491318, -98.37317400519893),
    (40.887254909662055, -98.37317892995024),
    (40.88673615464531, -98.37324787646557),
    (40.886482980859384, -98.37323638537788),
    (40.88545290107626, -98.37333652198858),
    (40.88540822255482, -98.37384377135761),
    (40.88527170465601, -98.3742295435631),
    (40.88498005184619, -98.37464486425907),
    (40.88471942485049, -98.3748763275634),
    (40.8844575557321, -98.37498303051221),
    (40.88412121995178, -98.37503063644006),
    (40.88373647949922, -98.3749108008285),
    (40.88368683540823, -98.37514554730026)
    ]
interval_upper_bound = 25
# route = RouteClass(polyline_coordinates=polyline_coordinates, interval_upper_bound=interval_upper_bound)
route = RouteClass(polyline_coordinates=polyline_coordinates_2022_B_Loop, interval_upper_bound=interval_upper_bound)


"""
Step 2: Interpolate coordinates and coordinate info for our route
"""
polyline_coordinates = route.polyline_coordinates
interval_upper_bound = route.interval_upper_bound
coordinates = get_coordinates(polyline_coordinates=polyline_coordinates, interval_upper_bound=interval_upper_bound)

route.append_data(coordinates)
# print(route.data())
# route.get_csv("sample_route_step2")
# route.to_database(table_name="sample_route_step2")


"""
Step 3: Get elevation info for our route
"""
coordinates = route.coordinate_list()
elevations = get_elevations(coordinates=coordinates, BING_MAPS_API_KEY=BING_MAPS_API_KEY)

route.append_data(elevations)
# print(route.data())
# route.get_csv("sample_route_step3")
# route.to_database(table_name="sample_route_step3")


"""
Step 4: Map routebook data to RouteClass data
IMPORTANT: The route in RouteClass must be as percise as possible
IMPORTANT: The start point in the RouteClass route must be the same (or as close) as the routebook start point
IMPORTANT: The mapping routebook onto our route data has an accuracy/error upper bound of interval_upper_bound/2 
"""
trip_distance_list = route.listdata("trip(m)")
routebook_filepath = "/home/ryanlam/Desktop/strategy_xv/routemodelv2/sample_data/2022_B_Loop.csv"
bypass_dist_error = True # set to False when not in dev
mapped_routebook = map_routebook_data(trip_distance_list=trip_distance_list, routebook_filepath=routebook_filepath, bypass_dist_error=bypass_dist_error)

route.append_data(mapped_routebook)
# print(route.data())
route.get_csv("sample_route_step4")
# route.to_database(table_name="sample_route_step4")

