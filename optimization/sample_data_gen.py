import pandas as pd
import numpy as np

# Set a seed so that the random numbers are reproducible
np.random.seed(0)

# Number of data points
n = 100

# Generate random data
data = pd.DataFrame({
    'latitude': np.random.uniform(-90, 90, n),
    'longitude': np.random.uniform(-180, 180, n),
    'elevation': np.random.uniform(0, 2000, n),  # in meters
    'wind_speed': np.random.uniform(0, 30, n),  # in m/s
    'humidity': np.random.uniform(0, 1, n),  # relative humidity, 0-1
    'temperature': np.random.uniform(-20, 40, n),  # in Celsius
})

# Save to CSV
data.to_csv('race_track_data.csv', index=False)