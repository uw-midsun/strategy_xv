# Tools.py: General tools that may be useful throughout dev


## velocity_vector(speed, bearing, elevation_angle)
```
velocity_vector: creates a cartesian vector representing the velocity using spherical vector values (velocity, bearing, elevation_angle)
@param speed: the speed (a magnitude)
@param bearing: the direction bearing (in degrees) of the velocity (in x-y axis) where 0/360 degrees is North
@param elevation_angle: the elevation_angle of the velocity relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@return: np.array representing a 3d vector
```

## velocity_projection(vector_1, vector_2)
```
velocity_projection: calculates the projection of vector_2 onto vector_1 in the vector_1 direction
@param vector_1: A vector represented by a np.array
@param vector_2: A vector represented by a np.array
@return: Vector that is the projection of vector_2 onto vector_1 in the vector_1 direction

```
