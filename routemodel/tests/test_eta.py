import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import pandas as pd
from eta.eta import ETA


"""
- Test eta functions from /eta/eta.py
"""


coords = [
    [43.46786317655638, -80.56637564010215],
    [43.48175280991097, -80.52637854159468],
    [43.48536483714299, -80.5270651870626],
    [43.48511573875007, -80.52869597004897],
    [43.48536483714299, -80.52989759961787],
    [43.48604985242712, -80.5304984144023],
    [43.48816712335336, -80.5320433668198],
    [43.489910702452285, -80.53461828732458],
    [43.49196557034531, -80.53762236124682],
    [43.494347261633344, -80.5482439084337]
]
eta = ETA(coords)

# Tests if the eta object is properly segmenting the given race route
def test_checkpoint_generation():
    assert(isinstance(eta.checkpoint_coords, list) and len(eta.checkpoint_coords) == 7)

# Tests if the eta object is returning the proper amount of arribal times
def test_eta_times():
    eta.update_checkpoint(43.46786317655638, -80.56637564010215, full_scan=True) # The checkpoint must be updated to get an accurate eta
    arrival_times = eta.get_eta()
    assert(isinstance(arrival_times, list) and len(arrival_times) == 7)

# Tests if the eta object can successfully update the car's location
def test_location_update():
    assert(eta.update_location())