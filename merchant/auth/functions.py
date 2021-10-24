from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
import time

from database import initDatabaseConnection

class MerchantRegister(Resource):
    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)
    
    def post(self):
        merchantParser = reqparse.RequestParser(bundle_errors=True, trim=True)
        merchantParser.add_argument('merchant_email', type=str, required=True, help="This is required field. [type=string]")
        merchantParser.add_argument('merchant_wallet_address', type=str, required=True, help="This is required field. [type=string]")
        merchantParser.add_argument('merchant_shop_name', type=str, required=True, help="This is required field. [type=string]")
        merchantParser.add_argument('merchant_phone_number', type=str, required=True, help="This is required field. [type=string]")
        data = merchantParser.parse_args()

        merchant_email = (data['merchant_email'].strip()).lower()
        merchant_wallet_address = data['merchant_wallet_address']

        self.cursor.execute("SELECT * FROM merchants WHERE merchants.merchant_email = '{}'".format(merchant_email))
        countMerchant = self.cursor.fetchall()

        if len(countMerchant) > 0 :
            return {
                "valid" : False,
                "msg": "{} already exists on our system. please do not register again.".format(merchant_email)
            }
        
        self.cursor.execute("SELECT * FROM merchants WHERE merchants.merchant_wallet_address = '{}'".format(merchant_wallet_address))
        countWalletAddress = self.cursor.fetchall()

        if len(countWalletAddress) > 0:
            return {
                "valid" : False,
                "msg": "{} already exists on our system. please do not register again.".format(merchant_wallet_address)
            }

        self.cursor.execute("INSERT INTO merchants SET merchant_email = '{}', merchant_wallet_address = '{}', merchant_shop_name = '{}', merchant_phone_number = '{}'".format(merchant_email, merchant_wallet_address, data['merchant_shop_name'], data['merchant_phone_number']))
        self.dbConn.commit()
        self.dbConn.close()

        if self.cursor.rowcount > 0:
            return {
                "valid": True,
                "merchant_id": self.cursor.lastrowid,
                "merchant_email": merchant_email,
                "merchant_shop_name": data['merchant_shop_name'],
                "merchant_phone_number" : data['merchant_phone_number'],
                "merchant_wallet_address": merchant_wallet_address,
                "access_token" : create_access_token(identity= merchant_email + merchant_wallet_address),
                "expired_on": int(time.time()) + (86400 * 3)
            }


class MerchantLogin(Resource):
    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)
    
    def post(self):
        merchantParser = reqparse.RequestParser()
        merchantParser.add_argument("wallet_address", type=str, required=True,
                                help="This is required field. [type=string]")
        data = merchantParser.parse_args()
        
        self.cursor.execute("SELECT * FROM merchants WHERE merchants.merchant_wallet_address = '{}'".format(data['wallet_address']))
        merchantResult = self.cursor.fetchall()
        self.dbConn.close()

        if len(merchantResult) > 0:
            merchantResult = merchantResult[0]
            return {
                "valid": True,
                "merchant_id": merchantResult['merchant_id'],
                "merchant_email": merchantResult['merchant_email'],
                "merchant_shop_name": merchantResult['merchant_shop_name'],
                "merchant_phone_number" : merchantResult['merchant_phone_number'],
                "merchant_wallet_address": merchantResult['merchant_wallet_address'],
                "access_token" : create_access_token(identity= merchantResult['merchant_email'] +  merchantResult['merchant_wallet_address']),
                "expired_on": int(time.time()) + (86400 * 3)
            }
        return {
            "valid": False,
            "msg": "Account do not exists, please register."
        }, 200