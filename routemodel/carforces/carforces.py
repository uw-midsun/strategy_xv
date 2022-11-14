import numpy as np


# Forces are relative to the car (and not a flat surface/earth)

"""
DRAG FORCE CALCULATIONS (WORK IN PROGRESS)
"""

def velocity_vector(speed, bearing, elevation):
    """
    Creates a cartesian vector representing the velocity using spherical vector values (velocity, bearing, elevation)
    speed is the speed (a magnitude)
    bearing is the direction bearing (in degrees) of the velocity (in x-y axis) where 0/360 degrees is North
    elevation is the elevation of the velocity relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
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

    def elevation_to_phi(elevation):
        """
        Convert elevation to phi angles (radians) for calculating vectors
        """
        if not -90 <= elevation <= 90:
            raise TypeError("elevation must be within -90 to 90 degrees")
        return np.radians(90 - elevation)

    theta_radians = bearing_to_theta(bearing)
    phi_radians = elevation_to_phi(elevation)
    
    x = speed * np.cos(theta_radians) * np.sin(phi_radians)
    y = speed * np.sin(theta_radians) * np.sin(phi_radians)
    z = speed * np.cos(phi_radians)
    return np.array([x, y, z])
# print(velocity_vector(100, 90, 0))


def velocity_projection(v_car, v_car_bearing, v_car_elevation, v_wind, v_wind_bearing, v_wind_elevation):
    """
    Calculates the velocity vector of the car relative to the fluid (wind) reference frame when accounting for wind speed and direction
    v_car is the car speed (a magnitude)
    v_car_bearing is the car direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_car_elevation is the car elevation relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    v_wind is the wind speed (a magnitude)
    v_wind_bearing is the wind direction bearing in degrees (in x-y axis) where 0/360 degrees is North
    v_wind_elevation is the wind elevation relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    """

    velocity_vector_car = velocity_vector(v_car, v_car_bearing, v_car_elevation)
    velocity_vector_wind = velocity_vector(v_wind, v_wind_bearing, v_wind_elevation)

    projection = np.dot(velocity_vector_wind, velocity_vector_car) / np.linalg.norm(velocity_vector_car)
    unit_vector = velocity_vector_car / np.linalg.norm(velocity_vector_car)
    project_v_wind_onto_v_car = projection * unit_vector # 3D projection: https://www.youtube.com/watch?v=DfIsa7ArxSo

    # print(velocity_vector_car.tolist())
    # print(velocity_vector_wind.tolist())
    # print(project_v_wind_onto_v_car.tolist())
    # print((velocity_vector_car + project_v_wind_onto_v_car).tolist())
    return velocity_vector_car + project_v_wind_onto_v_car
# velocity_projection(1, 90, -10, 0.5, 45, 45)



def drag_coefficent():
    ...

def x_force_drag():
    ...


"""
GRAVITATIONAL FORCE CALCULATIONS
"""


"""
FRICTIONAL FORCE CALCULATIONS
"""


"""
DOWNFORCE CALCULATIONS
"""