import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import pandas as pd
from eta.eta import ETAQuery


"""
- Test ETAQuery functions from /eta/eta.py
"""

# The tests assume that the route model and checkpoint data are generated from the following route
ROUTE = [
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


# Tests if the eta query has the proper amount of checkpoints
def test_eta_generation():
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    CHECKPOINT_MODEL_PATH = os.path.normpath(os.path.join(DIR_PATH, '../data/checkpoint_model_db.csv'))
    checkpoint_model = pd.read_csv(CHECKPOINT_MODEL_PATH)
    ETAQ = ETAQuery(43.48175280991097, -80.52637854159468)
    times = ETAQ.get_times()

    assert(len(times) == len(checkpoint_model))

# Tests if the eta object can successfully update the car's location
def test_eta_time_to_point():
    ETAQ = ETAQuery(43.48175280991097, -80.52637854159468)
    time_to_point = ETAQ.get_time_to_point(43.489910702452285, -80.53461828732458)
    assert(type(time_to_point) == float and time_to_point > 0) 
