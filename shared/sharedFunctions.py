from flask_restful import Resource
import ipfsApi

from database import initDatabaseConnection

class getStateList(Resource):

    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    def get(self):
        self.cursor.execute("SELECT * FROM state")
        stateResult = self.cursor.fetchall()
        return stateResult

class ipfs(Resource):

    def __init__(self):
        self.api = ipfsApi.Client(host="https://ipfs.infura.io")

    def post(self):
        response = self.api.add_json({'test': 1})
        return response
