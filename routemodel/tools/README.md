# Tools.py: General tools that may be useful throughout dev


## velocity_vector(speed, bearing, elevation_angle)
```
velocity_vector: creates a cartesian vector representing the velocity using spherical vector values (velocity, bearing, elevation_angle)
@param speed: the speed (a magnitude)
@param bearing: the direction bearing (in degrees) of the velocity (in x-y axis) where 0/360 degrees is North
@param elevation_angle: the elevation_angle of the velocity relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@return: np.array representing a 3d vector
```
Let's say you have a car going Northeast (so 45 degrees) at 10m/s and at an angle +45 degrees to the ground. You would have `spped=10`, `bearing=45`, and `elevation_angle=45`. Using these values, you would get `velocity_vector(speed=10, bearing=45, elevation_angle=45)` and a result of `np.array([5, 5, 7.07106781])`

## vector_projection(vector_1, vector_2)
```
vector_projection: calculates the projection of vector_2 onto vector_1 in the vector_1 direction
@param vector_1: A vector represented by a np.array
@param vector_2: A vector represented by a np.array
@return: Vector that is the projection of vector_2 onto vector_1 in the vector_1 direction

```
Let's say you have 2 vectors: `vector_1 = np.array([1, 0, 3])` and `vector_2 = np.array([-1, 4, 2])`. You would like to find the projection of `vector_2` on `vector_1`, so you would use: `vector_projection(vector_1=np.array([1, 0, 3]), vector_2=np.array([-1, 4, 2]))` and get a result of `np.array([0.5, 0, 1.5])`

