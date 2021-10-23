from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required

from database import initDatabaseConnection

class UserMyAccountProfile(Resource):

    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)
    
    @jwt_required()
    def get(self):
        wallet_address = request.args.get('wallet_address')
        if wallet_address.strip() is "":
            return {
                "valid": False,
                "msg": "Please provide the wallet_address to continue."
            }
        
        self.cursor.execute("SELECT users.user_fullname, users.user_email, users.user_wallet_address FROM users WHERE users.user_wallet_address = '{}'".format(wallet_address))
        userDetail = self.cursor.fetchall()
        self.dbConn.close()
        if len(userDetail) is 0:
            return {
                "valid": False,
                "msg": "{} doesn't exist.".format(wallet_address)
            }
        
        userDetail[0]['valid'] = True
        return userDetail[0]

    @jwt_required()
    def put(self):
        userProfileParser = reqparse.RequestParser(bundle_errors=True, trim=True)
        userProfileParser.add_argument('wallet_address', type=str, required=True,
                                help="This is required field. [type=string]")
        userProfileParser.add_argument('user_fullname', type=str, required=True,
                                help="This is required field. [type=string]")
        data = userProfileParser.parse_args()
        wallet_address = data['wallet_address']

        self.cursor.execute("SELECT users.user_fullname, users.user_email, users.user_wallet_address FROM users WHERE users.user_wallet_address = '{}'".format(wallet_address))
        userCount = self.cursor.fetchall()

        if len(userCount) == 0:
          return {
                "valid": False,
                "msg": "{} doesn't exist.".format(wallet_address)
            }

        self.cursor.execute("UPDATE users SET users.user_fullname = '{}', user_updated_at = CURRENT_TIMESTAMP() WHERE users.user_wallet_address = '{}'".format(data['user_fullname'], wallet_address))
        self.dbConn.commit()
        self.dbConn.close()

        return {
            "valid": True
        }
