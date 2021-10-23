from flask_restful import Resource

from database import initDatabaseConnection

class getStateList(Resource):

    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    def get(self):
        self.cursor.execute("SELECT * FROM state")
        stateResult = self.cursor.fetchall()
        return stateResult
