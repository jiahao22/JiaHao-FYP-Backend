import mysql.connector


def initDatabaseConnection():
    # Localhost
    # dbConn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database='ecommerce',
    #     port=3307
    # )
    
    # Server
    dbConn = mysql.connector.connect(
        host="localhost",
        user="zhentong",
        password="yjp!fgv.kzf9BPA2dat",
        database='ecommerce',
        port=3306
    )
    return dbConn
