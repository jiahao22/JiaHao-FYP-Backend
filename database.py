import mysql.connector


def initDatabaseConnection():
    dbConn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='ecommerce',
        port=3307
    )
    return dbConn
