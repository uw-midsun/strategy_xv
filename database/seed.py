import mysql.connector

# Create connection to database
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="midsun_dev_db",
)
db = mydb.cursor()

# Delete all pre-existing data
db.execute("DROP DATABASE midsun_dev_db")
db.execute("CREATE DATABASE midsun_dev_db")

# Create tables
db.execute("USE midsun_dev_db")
db.execute("CREATE TABLE tablename1 (column1 VARCHAR(128), column2 VARCHAR(128))")
