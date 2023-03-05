import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import numpy as np
from tools.tools import velocity_vector, vector_projection




# Works in progress (WIP) and notes
# - All WIP need car specs from other subteams (or if they can just give us the coefficients directly)
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
    @param car_mass: mass of the car
    @param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    @param gravity: gravitational acceleration on earth
    @return: force of gravity in the x-direction relative to the car
    """
    return -car_mass * gravity * np.sin(np.radians(elevation_angle))


def y_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the force of gravity in the y-direction relative to the car (-ve as force is always pushing down)
    @param car_mass: mass of the car
    @param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    @param gravity: gravitational acceleration on earth
    @return: force of gravity in the y-direction relative to the car
    """
    return -car_mass * gravity * np.cos(np.radians(elevation_angle))


def y_force_normal(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the normal in the y-direction relative to the car (+ve as force is always pushing up)
    @param car_mass: mass of the car
    @param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    @param gravity: gravitational acceleration on earth
    @return: normal force in the y-direction relative to the car
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
    @param car_mass: mass of the car
    @param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    @param coef_resistance: the rolling resistance coefficient of the car
    @param gravity: gravitational acceleration on earth
    @return: the friction force in the x-direction relative to the car
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
    @param car_velocity_vector: a numpy array representing the velocity vector of the car (see tools/tools.velocity_vector)
    @param wind_velocity_vector: a numpy array representing the velocity vector of the wind (see tools/tools.velocity_vector)
    @param car_cross_sectional_area: the cross sectional area of the car when looking directly at the front of the car
    @param fluid_density: the fluid density (air density)
    @param drag_coefficent: the drag coefficent of the car
    @return: the drag force of the car due to the fluid (wind) in the x-direction relative to the car
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
    @param car_velocity_vector: a numpy array representing the velocity vector of the car (see tools/tools.velocity_vector)
    @param wind_velocity_vector: a numpy array representing the velocity vector of the wind (see tools/tools.velocity_vector)
    @param wing_area: the cross sectional area of the car when looking directly down the car (the entire car is treated as a wing)
    @param fluid_density: the fluid density (air density)
    @param lift_coefficent: the lift coefficent of the car
    @return: the down force of the car due to the fluid (wind) in the y-direction relative to the car
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
    @param car_mass: mass of the car
    @param car_vi_vector: a numpy array representing the initial velocity vector of the car (see tools/tools.velocity_vector)
    @param car_vf_vector: a numpy array representing the final velocity vector of the car (see tools/tools.velocity_vector)
    @param timedelta: the time difference between the inital and final velocities
    @return: the applied force in the x-direction relative to the car
    """
    assert type(car_vi_vector) == np.ndarray and len(car_vi_vector) == 3
    assert type(car_vf_vector) == np.ndarray and len(car_vf_vector) == 3

    # Get resultant vector and get resultant vector in the x-direction (relative to car)
    resultant_vector = car_vf_vector - car_vi_vector
    resultant_vector_projection = vector_projection(car_vi_vector, resultant_vector)

    accelration_vector = resultant_vector_projection / timedelta
    applied_force = np.linalg.norm(car_mass * accelration_vector)

    if np.dot(car_vi_vector, resultant_vector) < 0: # Check force in +ve or -ve x-direction relative to the car
        return -1 * applied_force
    else:
        return applied_force




if __name__ == "__main__":
    pass
