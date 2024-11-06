import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Mee1074$'
)

cursorObject = dataBase.cursor()

cursorObject.execute("use govsar;")
cursorObject.execute("drop database govsar;")
cursorObject.execute("create database govsar;")

print("ho Gaya!")