import numpy as np
from functools import lru_cache


# Works in progress (WIP) and notes
# - WIP: Calculate rolling_resistance_coefficient, https://en.wikipedia.org/wiki/Rolling_resistance#Rolling_resistance_coefficient
# - WIP: Calculate drag_coefficent, https://en.wikipedia.org/wiki/Drag_coefficient
# - WIP: Calculate lift_coefficent, https://en.wikipedia.org/wiki/Lift_coefficient
# - WIP: Better way of finding the applied force (smaller timedelta or calculate using motor force values or something...)
# - Refactor code to have them work with velocity vectors (reduces number of calculations and faster execution)
# - Consider using @lru_cache for some functions?
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
# print(x_force_gravity(10, -4))


def y_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the force of gravity in the y-direction relative to the car (-ve as force is always pushing down)
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    gravity is the gravitational acceleration on earth
    """
    return -car_mass * gravity * np.cos(np.radians(elevation_angle))
# print(y_force_gravity(10, -4))


def y_force_normal(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY):
    """
    Calculates the normal in the y-direction relative to the car (+ve as force is always pushing up)
    car_mass is mass of the car
    elevation_angle is the elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    gravity is the gravitational acceleration on earth
    """
    return -1 * y_force_gravity(car_mass, elevation_angle, gravity)
# print(y_force_normal(10, -4))




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
# print(x_force_friction(10, -4))




"""
DRAG AND DOWN FORCE CALCULATIONS (CLOSELY RELATED)
"""

@lru_cache # Cache results because used by x_force_drag and y_force_downforce
def velocity_vector(speed, bearing, elevation_angle):
    """
    Creates a cartesian vector representing the velocity using spherical vector values (velocity, bearing, elevation_angle)
    speed is the speed (a magnitude)
    bearing is the direction bearing (in degrees) of the velocity (in x-y axis) where 0/360 degrees is North
    elevation_angle is the elevation_angle of the velocity relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    """

    def bearing_to_theta(bearing): 
        """
        https://sciencing.com/calculate-angle-bearing-8655354.html
        Convert bearing to theta angles (radians) for calculating vectors
        """
        if not 0 <= bearing <= 360:
            raise TypeError("bear must be within 0 to 360 degrees")
        standard_angle = 90 - bearing
        if standard_angle < 0:
            standard_angle + 360
        elif standard_angle > 0:
            standard_angle - 360
        return np.radians(standard_angle)

    def elevation_angle_to_phi(elevation_angle):
        """
        Convert elevation_angle to phi angles (radians) for calculating vectors
        """
        if not -90 <= elevation_angle <= 90:
            raise TypeError("elevation_angle must be within -90 to 90 degrees")
        return np.radians(90 - elevation_angle)

    theta_radians = bearing_to_theta(bearing)
    phi_radians = elevation_angle_to_phi(elevation_angle)
    
    x = speed * np.cos(theta_radians) * np.sin(phi_radians)
    y = speed * np.sin(theta_radians) * np.sin(phi_radians)
    z = speed * np.cos(phi_radians)
    return np.array([x, y, z])
# print(velocity_vector(100, 90, 0))

@lru_cache # Cache results because used by x_force_drag and y_force_downforce
def velocity_projection(v_car, v_car_bearing, v_car_elevation_angle, v_wind, v_wind_bearing, v_wind_elevation_angle):
    """
    Calculates the velocity vector of the car relative to the fluid (wind) reference frame when accounting for wind speed and direction
    v_car is the car speed (a magnitude)
    v_car_bearing is the car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_car_elevation_angle is the car elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    v_wind is the wind speed (a magnitude)
    v_wind_bearing is the wind direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_wind_elevation_angle is the wind elevation_angle relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    """

    velocity_vector_car = velocity_vector(v_car, v_car_bearing, v_car_elevation_angle)
    velocity_vector_wind = velocity_vector(v_wind, v_wind_bearing, v_wind_elevation_angle)

    projection = np.dot(velocity_vector_wind, velocity_vector_car) / np.linalg.norm(velocity_vector_car)
    unit_vector = velocity_vector_car / np.linalg.norm(velocity_vector_car)
    project_v_wind_onto_v_car = projection * unit_vector # 3D projection: https://www.youtube.com/watch?v=DfIsa7ArxSo

    return velocity_vector_car + project_v_wind_onto_v_car
# print(velocity_projection(1, 90, -10, 0.5, 45, 45))


def drag_coefficent(): # WIP
    ... 


def x_force_drag(
    v_car, 
    v_car_bearing, 
    v_car_elevation_angle, 
    v_wind, 
    v_wind_bearing, 
    v_wind_elevation_angle, 
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
    car_fluid_velocity_vector = velocity_projection(v_car, v_car_bearing, v_car_elevation_angle, v_wind, v_wind_bearing, v_wind_elevation_angle)
    car_fluid_velocity_magnitude = np.linalg.norm(car_fluid_velocity_vector)
    
    drag_force = 0.5 * fluid_density * np.square(car_fluid_velocity_magnitude) * drag_coefficent * car_cross_sectional_area
    return -1 * drag_force # Change to negative/positive to represent the force direction relative to the car
# print(x_force_drag(1, 90, -10, 0.5, 45, 45, 100, 1.204, 1))


def lift_coefficent(): # WIP
    ...


def y_force_downforce(
    v_car, 
    v_car_bearing, 
    v_car_elevation_angle, 
    v_wind, 
    v_wind_bearing, 
    v_wind_elevation_angle,
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
    car_fluid_velocity_vector = velocity_projection(v_car, v_car_bearing, v_car_elevation_angle, v_wind, v_wind_bearing, v_wind_elevation_angle)
    car_fluid_velocity_magnitude = np.linalg.norm(car_fluid_velocity_vector)

    downforce = lift_coefficent * 0.5 * fluid_density * np.square(car_fluid_velocity_magnitude) * wing_area
    return -1 * downforce # Change to negative/positive to represent the force direction relative to the car
# print(y_force_downforce(1, 90, -10, 0.5, 45, 45, 100, 1.204, 1))




"""
APPLIED FORCE CALCULATIONS
"""

def x_force_applied(car_mass, vi_car, vi_car_bearing, vi_car_elevation_angle, vf_car, vf_car_bearing, vf_car_elevation_angle, timedelta):
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
    car_vi_vector = velocity_vector(vi_car, vi_car_bearing, vi_car_elevation_angle)
    car_vf_vector = velocity_vector(vf_car, vf_car_bearing, vf_car_elevation_angle)

    # Get resultant vector and get resultant vector in the x-direction (relative to car)
    resultant_vector = car_vf_vector - car_vi_vector
    projection = np.dot(resultant_vector, car_vi_vector) / np.linalg.norm(car_vi_vector)
    unit_vector = car_vi_vector / np.linalg.norm(car_vi_vector)
    velocity_projection = projection * unit_vector # 3D projection: https://www.youtube.com/watch?v=DfIsa7ArxSo

    return np.linalg.norm(car_mass * (velocity_projection / timedelta))
# print(x_force_applied(100, 1, 90, -45, 2, 0, 45, 5))




if __name__ == "__main__":
    pass
