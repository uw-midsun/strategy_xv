import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import pytest
import numpy as np
from carforces.carforces import *




class Test_Gravitational_Normal_Forces():

    def test_x_force_gravity(self):
        EARTH_GRAVITY = 9.80665

        gravity_1 = x_force_gravity(car_mass=100, elevation_angle=0, gravity=EARTH_GRAVITY)
        correct_gravity_1 = 0
        np.isclose(gravity_1, correct_gravity_1)

        gravity_2 = x_force_gravity(car_mass=100, elevation_angle=10, gravity=10)
        correct_gravity_2 = -173.6481777
        np.isclose(gravity_2, correct_gravity_2)

        gravity_3 = x_force_gravity(car_mass=10, elevation_angle=-10, gravity=10)
        correct_gravity_3 = 17.36481777
        np.isclose(gravity_3, correct_gravity_3)


    def test_y_force_gravity(self):
        EARTH_GRAVITY = 9.80665

        gravity_1 = y_force_gravity(car_mass=100, elevation_angle=0, gravity=EARTH_GRAVITY)
        correct_gravity_1 = -980.665
        np.isclose(gravity_1, correct_gravity_1)

        gravity_2 = y_force_gravity(car_mass=100, elevation_angle=10, gravity=10)
        correct_gravity_2 = -984.807753
        np.isclose(gravity_2, correct_gravity_2)

        gravity_3 = y_force_gravity(car_mass=10, elevation_angle=-10, gravity=10)
        correct_gravity_3 = -984.807753
        np.isclose(gravity_3, correct_gravity_3)


    def test_y_force_normal(self):
        EARTH_GRAVITY = 9.80665

        gravity_1 = y_force_normal(car_mass=100, elevation_angle=0, gravity=EARTH_GRAVITY)
        correct_gravity_1 = 980.665
        np.isclose(gravity_1, correct_gravity_1)

        gravity_2 = y_force_normal(car_mass=100, elevation_angle=10, gravity=10)
        correct_gravity_2 = 984.807753
        np.isclose(gravity_2, correct_gravity_2)

        gravity_3 = y_force_normal(car_mass=10, elevation_angle=-10, gravity=10)
        correct_gravity_3 = -984.807753
        np.isclose(gravity_3, correct_gravity_3)




class Test_Frictional_Forces():
    
    @pytest.mark.skip(reason="rolling_resistance_coefficient function is not complete")
    def test_rolling_resistance_coefficient(self):
        ...


    def test_x_force_friction(self):
        ROLLING_RESISTANCE_COEFFICIENT = 2 # Dummy value
        EARTH_GRAVITY = 9.80665

        friction_1 = x_force_friction(car_mass=100, elevation_angle=0, coef_resistance=ROLLING_RESISTANCE_COEFFICIENT, gravity=EARTH_GRAVITY)
        correct_friction_1 = -1961.33
        np.isclose(friction_1, correct_friction_1)

        friction_2 = x_force_friction(car_mass=100, elevation_angle=10, coef_resistance=123, gravity=10)
        correct_friction_2 = -121131.353619
        np.isclose(friction_2, correct_friction_2)

        friction_3 = x_force_friction(car_mass=100, elevation_angle=-10, coef_resistance=0.5, gravity=10)
        correct_friction_3 = -492.4038765
        np.isclose(friction_3, correct_friction_3)




class Test_Drag_Down_Forces():

    @pytest.mark.skip(reason="drag_coefficent function is not complete")
    def test_drag_coefficent(self):
        ...

    def test_x_force_drag(self):
            AIR_DENSITY = 1.204
            DRAG_COEFFICIENT = 1
            return
            car_velocity_vector = np.array([])
            wind_velocity_vector = np.array([])
            car_cross_sectional_area = 100
            drag_1 = x_force_drag(car_velocity_vector, wind_velocity_vector, car_cross_sectional_area, fluid_density=AIR_DENSITY, drag_coefficent=DRAG_COEFFICIENT)
            correct_drag_1 = None
            ...