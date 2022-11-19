import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import numpy as np
from tools.tools import *




def test_velocity_vector():
    vector_1 = velocity_vector(10, 45, 45)
    correct_vector_1 = np.array([5, 5, 7.07106781])
    np.testing.assert_array_almost_equal(vector_1, correct_vector_1)

    vector_2 = velocity_vector(10, 90, -90)
    correct_vector_2 = np.array([0, 0, -10])
    np.testing.assert_array_almost_equal(vector_2, correct_vector_2)


def test_vector_projection():
    vector_1 = np.array([10, 0, 0])
    vector_2 = np.array([-10, 10, 10])
    projection_12 = vector_projection(vector_1, vector_2)
    correct_projection_12 = np.array([-10, 0, 0])
    np.testing.assert_array_almost_equal(projection_12, correct_projection_12)

    vector_3 = np.array([1, 0, 3])
    vector_4 = np.array([-1, 4, 2])
    projection_34 = vector_projection(vector_3, vector_4)
    correct_projection_34 = np.array([0.5, 0, 1.5])
    np.testing.assert_array_almost_equal(projection_34, correct_projection_34)
    
    