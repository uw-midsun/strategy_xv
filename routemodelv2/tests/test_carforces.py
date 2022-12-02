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

        car_velocity_vector_1 = np.array([1, 0, 3])
        wind_velocity_vector_1 = np.array([-1, 4, 2])
        car_cross_sectional_area_1 = 100
        drag_1 = x_force_drag(car_velocity_vector_1, wind_velocity_vector_1, car_cross_sectional_area_1, fluid_density=AIR_DENSITY, drag_coefficent=DRAG_COEFFICIENT)
        correct_drag_1 = -150.5
        np.isclose(drag_1, correct_drag_1)

        car_velocity_vector_2 = np.array([1, 0, 0])
        wind_velocity_vector_2 = np.array([0, 1, 0])
        car_cross_sectional_area_2 = 100
        drag_2 = x_force_drag(car_velocity_vector_2, wind_velocity_vector_2, car_cross_sectional_area_2, fluid_density=AIR_DENSITY, drag_coefficent=DRAG_COEFFICIENT)
        correct_drag_2 = 0
        np.isclose(drag_2, correct_drag_2)

        car_velocity_vector_3 = np.array([3, 1, -2])
        wind_velocity_vector_3 = np.array([2, 3, 1])
        car_cross_sectional_area_3 = 123
        drag_3 = x_force_drag(car_velocity_vector_3, wind_velocity_vector_3, car_cross_sectional_area_3, fluid_density=1.5, drag_coefficent=1.5)
        correct_drag_3 = -484.3125
        np.isclose(drag_3, correct_drag_3)


    @pytest.mark.skip(reason="lift_coefficent function is not complete")
    def test_lift_coefficent(self):
        ...
    

    def test_y_force_downforce(self):
        AIR_DENSITY = 1.204
        LIFT_COEFFICIENT = 2

        car_velocity_vector_1 = np.array([1, 0, 3])
        wind_velocity_vector_1 = np.array([-1, 4, 2])
        wing_area_1 = 100
        downforce_1 = y_force_downforce(car_velocity_vector_1, wind_velocity_vector_1, wing_area_1, fluid_density=AIR_DENSITY, lift_coefficent=LIFT_COEFFICIENT)
        correct_downforce_1 = -301
        np.isclose(downforce_1, correct_downforce_1)

        car_velocity_vector_2 = np.array([1, 0, 0])
        wind_velocity_vector_2 = np.array([0, 1, 0])
        wing_area_2 = 100
        downforce_2 = y_force_downforce(car_velocity_vector_2, wind_velocity_vector_2, wing_area_2, fluid_density=AIR_DENSITY, lift_coefficent=LIFT_COEFFICIENT)
        correct_downforce_2 = 0
        np.isclose(downforce_2, correct_downforce_2)

        car_velocity_vector_3 = np.array([3, 1, -2])
        wind_velocity_vector_3 = np.array([2, 3, 1])
        wing_area_3 = 321
        downforce_3 = y_force_downforce(car_velocity_vector_3, wind_velocity_vector_3, wing_area_3, fluid_density=1.5, lift_coefficent=1.5)
        correct_downforce_3 = -1263.9375
        np.isclose(downforce_3, correct_downforce_3)




class Test_Applied_Force():

    def test_x_force_applied(self):

        mass_1 = 100
        car_vi_vector_1 = np.array([1, 1, 2])
        car_vf_vector_1 = np.array([1, 1, 2])
        timedelta_1 = 1
        applied_force_1 = x_force_applied(mass_1, car_vi_vector_1, car_vf_vector_1, timedelta_1)
        correct_applied_force_1 = 0
        np.isclose(applied_force_1, correct_applied_force_1)
        
        mass_2 = 123
        car_vi_vector_2 = np.array([-1, -3, -2])
        car_vf_vector_2 = np.array([4, 4, 3])
        timedelta_2 = 0.5
        applied_force_2 = x_force_applied(mass_2, car_vi_vector_2, car_vf_vector_2, timedelta_2)
        correct_applied_force_2 = -2366.865558
        np.isclose(applied_force_2, correct_applied_force_2)

        mass_3 = 10
        car_vi_vector_3 = np.array([1, 0, 0])
        car_vf_vector_3 = np.array([-2, 1, -1])
        timedelta_3 = 0.25
        applied_force_3 = x_force_applied(mass_3, car_vi_vector_3, car_vf_vector_3, timedelta_3)
        correct_applied_force_3 = 0
        np.isclose(applied_force_3, correct_applied_force_3)

        mass_4 = 50
        car_vi_vector_4 = np.array([1 ,3, 2])
        car_vf_vector_4 = np.array([4, 4, 3])
        timedelta_4 = 2
        applied_force_4 = x_force_applied(mass_4, car_vi_vector_4, car_vf_vector_4, timedelta_4)
        correct_applied_force_4 = 53.45224838
        np.isclose(applied_force_4, correct_applied_force_4)