# Optimization

## Goal

The goal of this project is to find the optimal velocity of the vehicle at any given time based on the predicted net energy consumption of the vehicle. 

## Approach

Optimization algorithms utilize a Loss function (known as the objective) that needs to be minimized in order to find the value of the velocity at the global minimum of this loss function. 

From research done in this ticket: https://uwmidsun.atlassian.net/browse/STRAT15-28?atlOrigin=eyJpIjoiMjA1Y2QzZjhlMzI3NDI2MThjZTBiYzhmOTNlMWQwMjMiLCJwIjoiaiJ9 we have decided to go forward with **[`scipy.optimize.minimize()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)** with the `trust-constr` option for the minimize function. 

The objective function takes a `v_profile` and returns the energy used by the car. This is the loss function that the `optimize` function needs to minimize in order to find the optimal velocity which is the `x` variable of the solution. 

We start with the elevations and we calculate angle of elevations using the formula 

$$
\theta = \arctan(\dfrac{\text{elevation}}{\text{distance}})
$$

We create a list of these ‘pitches’ which is known as the `e_profile` .

Then we generate the initial profile using the following parameters:

```python
"""
    :param time: Maximum allowable time to cover a distance in seconds
    :param distance: Distance to be covered in meters
    :param e_profile: List of pitches the car must travel
    :param min_velocity: Minimum allowable velocity
    :param stop_profile: List of indices where car must stop
"""
```