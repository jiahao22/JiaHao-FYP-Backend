from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
import time

from database import initDatabaseConnection


class UserLogin(Resource):
    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    def post(self):
        userParser = reqparse.RequestParser(bundle_errors=True)
        userParser.add_argument("wallet_address", type=str, required=True,
                                help="This is required field. [type=string]")
        data = userParser.parse_args()

        self.cursor.execute(
            "SELECT * FROM users WHERE users.user_wallet_address = '{}'".format(data['wallet_address']))
        result = self.cursor.fetchall()
        self.dbConn.close()

        if len(result) > 0:
            return {
                "valid": True,
                "user_id": result[0]['user_id'],
                "user_email": result[0]['user_email'],
                "access_token": create_access_token(identity=data['wallet_address']),
                "wallet_address": data['wallet_address'],
                "expired_on": int(time.time()) + (86400 * 3)
            }, 200
        return {
            "valid": False,
            "msg": "Account do not exists, please register."
        }, 200


class UserRegister(Resource):
    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    def post(self):
        userParser = reqparse.RequestParser(trim=True, bundle_errors=True)
        userParser.add_argument('user_fullname', type=str, required=True,
                                help="This is required field. [type=string]")
        userParser.add_argument(
            'user_email', type=str, required=True, help="This is required field. [type=string]")
        userParser.add_argument('wallet_address', type=str, required=True,
                                help="This is required field. [type=string]")
        data = userParser.parse_args()

        user_fullname = data['user_fullname']
        user_email = (data['user_email'].strip()).lower()
        user_wallet_address = data['wallet_address']

        # Select user by the user_email
        self.cursor.execute(
            "SELECT * FROM users WHERE users.user_email = '{}'".format(user_email))
        result_check_email = self.cursor.fetchall()
        if len(result_check_email) > 0:
            return {
                "valid": False,
                "msg": "{} already exists, please try another email. ".format(user_email)
            }

        # Select user by the wallet address
        self.cursor.execute(
            "SELECT * FROM users WHERE users.user_wallet_address = '{}'".format(
                user_wallet_address)
        )
        result_check_wallet_address = self.cursor.fetchall()
        if len(result_check_wallet_address) > 0:
            return {
                "valid": False,
                "msg": "{} already exists on our system. please do not register again.".format(user_wallet_address)
            }

        # Insert into users
        self.cursor.execute("INSERT INTO users SET user_fullname = '{}', user_email = '{}', user_wallet_address = '{}'".format(
            user_fullname, user_email, user_wallet_address))
        self.dbConn.commit()
        self.dbConn.close()

        if self.cursor.rowcount > 0:
            return {
                "valid": True
            }
        return {
            "valid": False
        }


class UserCheckAccountExists(Resource):
    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    def post(self):
        userParser = reqparse.RequestParser(trim=True, bundle_errors=True)
        userParser.add_argument('wallet_address', type=str, required=True,
                                help="This is required field. [type=string]")
        data = userParser.parse_args()

        # Select the user by the wallet address.
        self.cursor.execute(
            "SELECT * FROM users WHERE users.user_wallet_address = '{}'".format(data['wallet_address']))
        result = self.cursor.fetchall()
        self.dbConn.close()

        if len(result) > 0:
            return {
                "accountExist": True
            }, 200
        return {
            "accountExist": False
        }
