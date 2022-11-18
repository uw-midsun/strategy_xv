import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import numpy as np
from tools.tools import velocity_vector, vector_projection


# Works in progress (WIP) and notes
# - WIP: Calculate rolling_resistance_coefficient, https://en.wikipedia.org/wiki/Rolling_resistance#Rolling_resistance_coefficient
# - WIP: Calculate drag_coefficent, https://en.wikipedia.org/wiki/Drag_coefficient
# - WIP: Calculate lift_coefficent, https://en.wikipedia.org/wiki/Lift_coefficient
# - WIP: Better way of finding the applied force (smaller timedelta or calculate using motor force values or something...)
# - Air density based on temp, humidity, pressure?
# - Consider motor efficiency and other efficiencies?


"""
Forces are relative to the car (and not a flat surface/earth)
- +ve force in x direction pushes car forward
- -ve force in x direction pushes car backward
- +ve force in y direction pushes car up
- -ve force in y direction pushes car down

Net x force: gravity force (x-direction) + applied force + friction force + drag force
Net y force: gravity force (y-direction) + normal force + downforce
"""




"""
CONSTANTS
"""
EARTH_GRAVITY = 9.80665 # m/s^2, average earth's gravity
ROLLING_RESISTANCE_COEFFICIENT = 1 # Placeholder value, Dimensionless
DRAG_COEFFICIENT = 1 # Placeholder value, Dimensionless
LIFT_COEFFICIENT = 1 # Placeholder value, Dimensionless
AIR_DENSITY = 1.204 # kg/m^3, Room temperature air density




"""
GRAVITATIONAL/NORMAL FORCE CALCULATIONS
"""

def x_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY): 
    """
    Calculates the force of gravity in the x-direction relative to the car (-ve force is pushing car backward, +ve force is pushing car forward)
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    gravity is the gravitational acceleration on earth
    """
    return -car_mass * gravity * np.sin(np.radians(elevation_angle))


def y_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the force of gravity in the y-direction relative to the car (-ve as force is always pushing down)
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    gravity is the gravitational acceleration on earth
    """
    return -car_mass * gravity * np.cos(np.radians(elevation_angle))


def y_force_normal(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the normal in the y-direction relative to the car (+ve as force is always pushing up)
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    gravity is the gravitational acceleration on earth
    """
    return -1 * y_force_gravity(car_mass, elevation_angle, gravity)




"""
FRICTIONAL FORCE CALCULATIONS
"""

def rolling_resistance_coefficient(): # WIP
    ...


def x_force_friction(car_mass, elevation_angle=0, coef_resistance=ROLLING_RESISTANCE_COEFFICIENT, gravity=EARTH_GRAVITY):
    """
    Calculates the friction (actually called rolling friction or rolling drag) of the car
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    coef_resistance is the rolling resistance coefficient of the car
    gravity is the gravitational acceleration on earth
    """
    return coef_resistance * y_force_normal(car_mass, elevation_angle, gravity)




"""
DRAG AND DOWN FORCE CALCULATIONS (CLOSELY RELATED)
"""

def drag_coefficent(): # WIP
    ... 


def x_force_drag(
    car_velocity_vector, 
    wind_velocity_vector,
    car_cross_sectional_area,
    fluid_density=AIR_DENSITY,
    drag_coefficent=DRAG_COEFFICIENT
    ):
    """
    Calculates the drag force of the car due to the fluid (wind)
    v_car is the car speed (a magnitude)
    v_car_bearing is the car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_car_elevation_angle is the car elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    v_wind is the wind speed (a magnitude)
    v_wind_bearing is the wind direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_wind_elevation_angle is the wind elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    car_cross_sectional_area is the cross sectional area of the car when looking directly at the front of the car
    fluid_density is the fluid density (air density)
    drag_coefficent is the drag coefficent of the car
    """
    assert type(car_velocity_vector) == np.ndarray and len(car_velocity_vector) == 3
    assert type(wind_velocity_vector) == np.ndarray and len(wind_velocity_vector) == 3

    car_fluid_velocity_vector = vector_projection(car_velocity_vector, wind_velocity_vector)
    car_fluid_velocity_magnitude = np.linalg.norm(car_fluid_velocity_vector)
    
    drag_force = 0.5 * fluid_density * np.square(car_fluid_velocity_magnitude) * drag_coefficent * car_cross_sectional_area
    return -1 * drag_force # Change to negative/positive to represent the force direction relative to the car


def lift_coefficent(): # WIP
    ...


def y_force_downforce(
    car_velocity_vector, 
    wind_velocity_vector,
    wing_area,
    fluid_density=AIR_DENSITY,
    lift_coefficent=LIFT_COEFFICIENT
    ):
    """
    Calculates the downforce of the car due to the fluid (wind)
    v_car is the car speed (a magnitude)
    v_car_bearing is the car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_car_elevation_angle is the car elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    v_wind is the wind speed (a magnitude)
    v_wind_bearing is the wind direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_wind_elevation_angle is the wind elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    wing_area is the cross sectional area of the car when looking directly down the car (the entire car is treated as a wing)
    fluid_density is the fluid density (air density)
    lift_coefficent is the lift coefficent of the car
    """
    assert type(car_velocity_vector) == np.ndarray and len(car_velocity_vector) == 3
    assert type(wind_velocity_vector) == np.ndarray and len(wind_velocity_vector) == 3

    car_fluid_velocity_vector = vector_projection(car_velocity_vector, wind_velocity_vector)
    car_fluid_velocity_magnitude = np.linalg.norm(car_fluid_velocity_vector)

    downforce = lift_coefficent * 0.5 * fluid_density * np.square(car_fluid_velocity_magnitude) * wing_area
    return -1 * downforce # Change to negative/positive to represent the force direction relative to the car




"""
APPLIED FORCE CALCULATIONS
"""

def x_force_applied(car_mass, car_vi_vector, car_vf_vector, timedelta):
    """
    calculate the applied force in the x direction (relative to the car) using f=ma
    car_mass is mass of the car
    vi_car is the initial car speed (a magnitude)
    vi_car_bearing is the initial car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    vi_car_elevation_angle is the initial car elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    vf_car is the final car speed (a magnitude)
    vf_car_bearing is the final car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    vf_car_elevation_angle is the final car elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    timedelta is the time difference between the inital and final velocities
    """
    assert type(car_vi_vector) == np.ndarray and len(car_vi_vector) == 3
    assert type(car_vf_vector) == np.ndarray and len(car_vf_vector) == 3

    # Get resultant vector and get resultant vector in the x-direction (relative to car)
    resultant_vector = car_vf_vector - car_vi_vector
    projection = np.dot(resultant_vector, car_vi_vector) / np.linalg.norm(car_vi_vector)
    unit_vector = car_vi_vector / np.linalg.norm(car_vi_vector)
    resultant_vector_projection = projection * unit_vector # 3D projection: https://www.youtube.com/watch?v=DfIsa7ArxSo

    return np.linalg.norm(car_mass * (resultant_vector_projection / timedelta))




if __name__ == "__main__":
    pass
