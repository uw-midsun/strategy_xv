import requests, math, psycopg2, pandas, sys, time

'''
API INFORMATION
Dataset Used: {srtm30m} https://www.opentopodata.org/datasets/srtm/
Parameters: Dataset, Coordinate <lat, long>
Return: Information returned as a json object [Elevation is in metres above sea level]
'''

'''
STEPS
1. Check if the “elevation” table exists, if it doesn't create it. If it does, move on.
2. Seed the database with a given CSV path of raw data (lats, and longs) 
3. Once seeded,  update the table for each lat and long entry with its:
    - elevation (as you have already captured)
    - degree of elevation
'''

FILENAME = None
DB_HOST = None
DB_NAME = None
DB_USER = None
DB_PASSWORD = None
DATASET = 'srtm30m'
QUERIES = {
    'create_table'      : "CREATE TABLE IF NOT EXISTS elevation (id SERIAL PRIMARY KEY, lat float8, lon float8, elevation float8, degree float8);",
    'clear_table'       : "TRUNCATE TABLE elevation RESTART IDENTITY;",
    'add_coord'         : "INSERT INTO elevation (lat, lon) VALUES (%s, %s)",
    'elevation_empty'   : "SELECT id, lat, lon FROM elevation WHERE elevation IS NULL",
    'degree_empty'      : "SELECT id, lat, lon FROM elevation WHERE degree IS NULL",
    'update_elevation'  : "UPDATE elevation SET elevation = %s WHERE id = %s",
    'udpate_degree'     : "UPDATE elevation SET degree = %s WHERE lat = %s AND lon = %s",
}

def verify_inputs():
    global FILENAME, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    if len(sys.argv) != 6:
        print("Usage: python elevation.py <filename.csv> <db_host> <db_name> <db_user> <db_password>")
        sys.exit(1)
    scriptname, filename, db_host, db_name, db_user, db_password = sys.argv
    FILENAME = filename
    DB_HOST = db_host
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASSWORD = db_password


def read_csv():
    df = pandas.read_csv(FILENAME)
    return df


def connect_to_db():
    connection = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    return connection


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(QUERIES['create_table'])
    connection.commit()
    cursor.close()
    print("table created!")
    return


def seed_database(connection, df):
    confirmation = input("Seeding the database will clear current values in the table. Would you like to continue? (Y/N): ").lower()
    if confirmation == "y":
        cursor = connection.cursor()
        print("Clearing table...")
        cursor.execute(QUERIES['clear_table'])
        connection.commit()
        print("Seeding Database...")
        for row in df.itertuples():
            lat = row.latitude
            lon = row.longitude
            cursor.execute(QUERIES['add_coord'], (lat, lon))
            connection.commit()
        cursor.close()
        print("Database seeded.")
        return True
    else:
        print("Operation canceled.")
        return False


def get_elevation(lat, long):
    parameter = f'{lat},{long}'
    try:
        response = requests.get(f'https://api.opentopodata.org/v1/{DATASET}?locations={parameter}&&interpolation=bilinear')
        response.raise_for_status()
        data = response.json()
        elevation_value = (data['results'][0]['elevation'])
        return elevation_value
    except Exception as e:
        print(repr(e))
        return


def calculate_degree(lat1, long1, elev1, lat2, long2, elev2):
    pass


def update_table_entries(connection):
    print("Updating table entries...")
    cursor = connection.cursor()
    # Check which rows have NULL elevation
    cursor.execute(QUERIES['elevation_empty'])
    rows_to_update = cursor.fetchall()
    for row in rows_to_update:
        id, lat, lon = row
        elevation = get_elevation(lat, lon)
        cursor.execute(QUERIES['update_elevation'], (elevation, id))
        connection.commit()
        print(f'Elevation Added for ID[{id}]')
        time.sleep(1)
    #TODO Update Degree
    cursor.close()
    return

# MAIN
if __name__ == "__main__":
    verify_inputs()
    df = read_csv()
    connection = connect_to_db()
    create_table(connection)
    seed_database(connection, df)
    update_table_entries(connection)
    connection.close()

