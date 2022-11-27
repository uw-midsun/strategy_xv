import os
import dotenv

import mysql.connector


dotenv.load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


connection = mysql.connector.connect(
  host=MYSQL_HOST,
  database="pets",
  user=MYSQL_USER,
  password=MYSQL_PASSWORD
)


if connection.is_connected():
  db_Info = connection.get_server_info()
  print("Connected to MySQL Server version ", db_Info)
  cursor = connection.cursor()
  cursor.execute("select database();")
  record = cursor.fetchone()
  print("You're connected to database: ", record)


print(connection)


if connection.is_connected():
  cursor.close()
  connection.close()
  print("MySQL connection is closed")
  