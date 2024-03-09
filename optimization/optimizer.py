import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('race_track_data.csv')

# Calculate distance
data['distance'] = 30 # in meters
# Calculate initial velocity profile
total_distance = np.sum(np.sqrt(np.diff(data['latitude'])**2 + np.diff(data['longitude'])**2))
# Calculate the angle of elevation
angle = np.arctan(np.diff(data['elevation']) / np.diff(data['distance']))
data['angle'] = np.insert(angle, 0, 0)  # Insert a 0 at the beginning to match the original length
total_time = 1  # replace with actual total time
data['velocity'] = total_distance / total_time
# Calculate elevation profile
data['elevation_diff'] = data['elevation'].diff()

# Constants
drag_coefficient = 0.5  # actual drag coefficient
car_area = 1  # car area in m^2
mu = 0.01  # coefficient of friction

# Calculate forces due to drag and friction
for i in range(len(data)):
    temperature = data.loc[i, 'temperature']
    humidity = data.loc[i, 'humidity']
    velocity = data.loc[i, 'velocity']
    theta = data.loc[i, 'angle']
    rho = 1.225 * (1 - (0.0065 * temperature) / 288.15) * (288.15 / (temperature + 273.15)) * (1 - humidity)
    drag_force = 0.5 * rho * velocity**2 * drag_coefficient * car_area
    friction_force = 9.81 * np.sin(theta) * mu
    data.loc[i, 'drag_force'] = drag_force
    data.loc[i, 'friction_force'] = friction_force

# Sliding window calculations
window_size = 10
for i in range(0, len(data) - window_size + 1):
    window_data = data.iloc[i:i+window_size]
    
# Placeholder for optimized velocities
optimized_velocities = []

# Loop over each window
for i in range(0, len(data) - window_size + 1):
    # Get the data for this window
    window_data = data.iloc[i:i+window_size]

    # Define the objective function for this window
    def objective_function(velocities, window_data):
        window_data['velocity'] = velocities
        average_velocity = np.mean(window_data['velocity'])
        average_drag_force = np.mean(window_data['drag_force'])
        average_friction_force = np.mean(window_data['friction_force'])
        average_power = average_velocity * (average_drag_force + average_friction_force)
        # To penalize large changes in velocity
        damping = 0.1 * np.sum(np.diff(velocities)**2)
        return average_power + damping

    # Initial guess is the current velocity profile for this window
    initial_guess = window_data['velocity'].values

    # Optimize the objective function for this window
    result = minimize(objective_function, initial_guess, args=(window_data,), method='Nelder-Mead')

    # Store the optimized velocities
    optimized_velocities.extend(result.x)

# Plot the optimized velocity profile
plt.plot(optimized_velocities)
plt.show()
