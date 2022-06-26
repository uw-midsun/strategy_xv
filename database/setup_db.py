import sqlite3

# creates database in /database directory
con = sqlite3.connect('strategy.db')

cur = con.cursor()
cur.execute('''CREATE TABLE routes 
            (latitude REAL, longitude REAL, maneuver_instruction TEXT, next_maneuver_distance REAL, direction REAL, street TEXT)''')
cur.execute('''CREATE TABLE elevations
            (latitude REAL, longitude REAL, elevation INTEGER)''')
cur.execute('''CREATE TABLE speedlimits
            (latitude REAL, longitude REAL, street TEXT, speedlimit INTEGER, speed_unit TEXT)''')

# as per current get_weather.py file
cur.execute('''CREATE TABLE weather
            (latitude REAL, longitude REAL, temperature REAL, wind_speed REAL, wind_direction INTEGER, weather_summary TEXT, weather_description TEXT, pressure REAL, precipitation REAL)''')

con.close()
