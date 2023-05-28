# Carforces.py

## Notes
- All forces are relative to the car (NOT the surface of the earth)
    - +ve force in x direction pushes car forward
    - -ve force in x direction pushes car backward
    - +ve force in y direction pushes car up
    - -ve force in y direction pushes car down
- Functions with an `x_` prefix calculate forces in the x-direction (relative to the car)
- Functions with an `y_` prefix calculate forces in the y-direction (relative to the car)
- We do not consider the forces on the sides of the car (where the passenger doors usually car)
- Net x force: gravity force (x-direction) + applied force + friction force + drag force
- Net y force: gravity force (y-direction) + normal force + downforce
- Constants are in full uppercase and see `carforces.py` for the most recent constant values
- **ALL VALUES MUST BE IN SI UNITS (METERS, KG, N, M/S, M/S^2, ETC...)**

## Works in progress (WIP) + considerations
- All WIP need car specs from other subteams (or if they can just give us the coefficients directly)
- WIP: Calculate rolling_resistance_coefficient, https://en.wikipedia.org/wiki/Rolling_resistance#Rolling_resistance_coefficient
- WIP: Calculate drag_coefficent, https://en.wikipedia.org/wiki/Drag_coefficient
- WIP: Calculate lift_coefficent, https://en.wikipedia.org/wiki/Lift_coefficient
- WIP: Better way of finding the applied force (smaller timedelta or calculate using motor force values or something...)
- Air density based on temp, humidity, pressure?
- Consider motor efficiency and other efficiencies?

---
## GRAVITATIONAL/NORMAL FORCE CALCULATIONS

### **Function:** x_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY)
```
Calculates the force of gravity in the x-direction relative to the car (-ve force is pushing car backward, +ve force is pushing car forward)
@param car_mass: mass of the car
@param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@param gravity: gravitational acceleration on earth
@return: force of gravity in the x-direction relative to the car
```

### **Function:** y_force_gravity(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY)
```
Calculates the force of gravity in the y-direction relative to the car (-ve as force is always pushing down)
@param car_mass: mass of the car
@param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@param gravity: gravitational acceleration on earth
@return: force of gravity in the y-direction relative to the car
```

### **Function:** y_force_normal(car_mass, elevation_angle=0, gravity=EARTH_GRAVITY)
```
Calculates the normal in the y-direction relative to the car (+ve as force is always pushing up)
@param car_mass: mass of the car
@param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@param gravity: gravitational acceleration on earth
@return: normal force in the y-direction relative to the car
```

## FRICTIONAL FORCE CALCULATIONS

### **Function:** rolling_resistance_coefficient()
```
WIP
```

### **Function:** x_force_friction(car_mass, elevation_angle=0, coef_resistance=ROLLING_RESISTANCE_COEFFICIENT, gravity=EARTH_GRAVITY)
```
Calculates the friction (actually called rolling friction or rolling drag) of the car
@param car_mass: mass of the car
@param elevation_angle: elevation_angle of the car relative to the x-axis (0 is on x-y plane, +ve is going up, -ve is going down)
@param coef_resistance: the rolling resistance coefficient of the car
@param gravity: gravitational acceleration on earth
@return: the friction force in the x-direction relative to the car
```

---
## DRAG AND DOWN FORCE CALCULATIONS (CLOSELY RELATED)

### **Function:** drag_coefficent()
```
WIP
```

### **Function:** x_force_drag(car_velocity_vector, wind_velocity_vector, car_cross_sectional_area, fluid_density=AIR_DENSITY, drag_coefficent=DRAG_COEFFICIENT)
```
Calculates the drag force of the car due to the fluid (wind)
@param car_velocity_vector: a numpy array representing the velocity vector of the car (see tools/tools.velocity_vector)
@param wind_velocity_vector: a numpy array representing the velocity vector of the wind (see tools/tools.velocity_vector)
@param car_cross_sectional_area: the cross sectional area of the car when looking directly at the front of the car
@param fluid_density: the fluid density (air density)
@param drag_coefficent: the drag coefficent of the car
@return: the drag force of the car due to the fluid (wind) in the x-direction relative to the car
```

### **Function:** lift_coefficent()
```
WIP
```

### **Function:** y_force_downforce(car_velocity_vector, wind_velocity_vector, wing_area, fluid_density=AIR_DENSITY, lift_coefficent=LIFT_COEFFICIENT)
```
Calculates the downforce of the car due to the fluid (wind)
@param car_velocity_vector: a numpy array representing the velocity vector of the car (see tools/tools.velocity_vector)
@param wind_velocity_vector: a numpy array representing the velocity vector of the wind (see tools/tools.velocity_vector)
@param wing_area: the cross sectional area of the car when looking directly down the car (the entire car is treated as a wing)
@param fluid_density: the fluid density (air density)
@param lift_coefficent: the lift coefficent of the car
@return: the down force of the car due to the fluid (wind) in the y-direction relative to the car
```

---
## APPLIED FORCE CALCULATIONS

### **Function:** x_force_applied(car_mass, car_vi_vector, car_vf_vector, timedelta)
```
calculate the applied force in the x direction (relative to the car) using f=ma
@param car_mass: mass of the car
@param car_vi_vector: a numpy array representing the initial velocity vector of the car (see tools/tools.velocity_vector)
@param car_vf_vector: a numpy array representing the final velocity vector of the car (see tools/tools.velocity_vector)
@param timedelta: the time difference between the inital and final velocities
@return: the applied force in the x-direction relative to the car
```