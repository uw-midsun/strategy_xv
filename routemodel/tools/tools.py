import numpy as np
from functools import lru_cache, wraps




# Core functions

def velocity_vector(speed, bearing, elevation_angle):
    """
    velocity_vector: creates a cartesian vector representing the velocity using spherical vector values (velocity, bearing, elevation_angle)
    @param speed: the speed (a magnitude)
    @param bearing: the direction bearing (in degrees) of the velocity (in x-y axis) where 0/360 degrees is North
    @param elevation_angle: the elevation_angle of the velocity relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
    @return: np.array representing a 3d vector
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

    assert speed > 0
    theta_radians = bearing_to_theta(bearing)
    phi_radians = elevation_angle_to_phi(elevation_angle)
    
    x = speed * np.cos(theta_radians) * np.sin(phi_radians)
    y = speed * np.sin(theta_radians) * np.sin(phi_radians)
    z = speed * np.cos(phi_radians)
    return np.array([x, y, z])


def velocity_projection(vector_1, vector_2):
    """
    velocity_projection: calculates the projection of vector_2 onto vector_1 in the vector_1 direction
    @param vector_1: A vector represented by a np.array
    @param vector_2: A vector represented by a np.array
    @return: Vector that is the projection of vector_2 onto vector_1 in the vector_1 direction
    """
    
    # 3D projection: https://www.youtube.com/watch?v=DfIsa7ArxSo
    projection = np.dot(vector_2, vector_1) / np.linalg.norm(vector_1)
    unit_vector = vector_1 / np.linalg.norm(vector_1)
    project_vector_2_onto_vector_1 = projection * unit_vector

    return project_vector_2_onto_vector_1




# Caching unhashable return values (numpy.ndarray is unhashable hence this work around))
def np_cache(function):
    @lru_cache()
    def cached_wrapper(hashable_array):
        array = np.array(hashable_array)
        return function(array)

    @wraps(function)
    def wrapper(array):
        return cached_wrapper(tuple(array))

    wrapper.cache_info = cached_wrapper.cache_info
    wrapper.cache_clear = cached_wrapper.cache_clear
    return wrapper

# Add your function here so it caches the results
np_cache(velocity_vector)
np_cache(velocity_projection)




if __name__ == "__main__":
    pass
