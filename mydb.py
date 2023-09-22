import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1997',
)

# preparing a cursor object

cursorObject = dataBase.cursor()

# create a database

cursorObject.execute("CREATE DATABASE yarobase")

print("Database created!")