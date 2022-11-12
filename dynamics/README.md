# Dynamics

Car manages the state of the car and uses these to calculate the forces applied
to the car.

## Car Class Functions

### The `force_req()` method

Computes the force in Newtons to have the car run at a given velocity. Based on the five forces acting upon it - force of aerodynamic drag, friction, braking, motors and gravity.

### The `max_velocity()` method

Computes the max velocity the car can go at a given time based on the force required.

### The `energy_used()` method

Computes the total energy used by the car given a series of velocities and a series of elevations.

## Coming Soon

Functions to parse old data.