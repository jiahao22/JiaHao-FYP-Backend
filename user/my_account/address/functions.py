from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required

from database import initDatabaseConnection

class UserAddress(Resource):

    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    @jwt_required()
    def get(self):
        user_id = request.args.get('user_id')
        address_id = request.args.get('address_id')

        if user_id == None or user_id.strip() == "":
            return {
                "valid" : False,
                "msg" : "Please provide the user_id to continue."
            }

        if address_id == None or address_id.strip() == "":
            return {
               "valid": False, 
               "msg": "Please provide the address_id to continue."
            }

        self.cursor.execute("SELECT address.address_id, address.address_fullname, address.address_phone_number, address.address_line1, address.address_line2, address.address_city, address.address_state, address.address_postcode, address.address_status FROM address WHERE address.address_user_id = '{}' AND address.address_id = '{}'".format(user_id, address_id))
        address = self.cursor.fetchall()
        self.dbConn.close()

        if len(address) > 0:
            address[0]['valid'] = True 
            return address[0]
        return {
            "valid" : False
        }

    @jwt_required()
    def post(self):
        addressParser = reqparse.RequestParser(bundle_errors=True)
        addressParser.add_argument('address_user_id', type=int, required=True, help="This field is required. [type=int]")
        addressParser.add_argument('address_fullname', type=str, required=True, help="This field is required. [type=string]")
        addressParser.add_argument('address_phone_number', type=str, required=True, help="This field is required. [type=string]")
        addressParser.add_argument('address_line1', type=str, required=True, help="This field is required. [type=string]")
        addressParser.add_argument('address_line2', type=str)
        addressParser.add_argument('address_city', type=str, required=True, help="This field is required. [type=string]")
        addressParser.add_argument('address_state', type=int, required=True, help="This field is required. [type=int]")
        addressParser.add_argument('address_postcode', type=str, required=True, help="This field is required. [type=string]")
        data = addressParser.parse_args()

        # Insert without address_line2
        if data['address_line2'] == None:
            self.cursor.execute("INSERT INTO address SET address_user_id = '{}', address_fullname = '{}', address_phone_number = '{}', address_line1 = '{}', address_city = '{}', address_state = '{}', address_postcode = '{}'".format(data['address_user_id'], data['address_fullname'], data['address_phone_number'], data['address_line1'], data['address_city'], data['address_state'], data['address_postcode']))
        else:
            self.cursor.execute("INSERT INTO address SET address_user_id = '{}', address_fullname = '{}', address_phone_number = '{}', address_line1 = '{}', address_line2 = '{}', address_city = '{}', address_state = '{}', address_postcode = '{}'".format(data['address_user_id'], data['address_fullname'], data['address_phone_number'], data['address_line1'], data['address_line2'], data['address_city'], data['address_state'], data['address_postcode']))
        self.dbConn.commit()
        self.dbConn.close()

        if self.cursor.rowcount > 0:
            return {
                'valid' : True,
                'address_id': self.cursor.lastrowid
            }
        return {
            'valid' : False
        }


    @jwt_required()
    def put(self):
        return

    @jwt_required()
    def delete(self):
        return

class UserGetAllAddress(Resource):

    def __init__(self):
        self.dbConn = initDatabaseConnection()
        self.cursor = self.dbConn.cursor(dictionary=True)

    @jwt_required()
    def get(self):
        user_id = request.args.get('user_id')

        if user_id == None or user_id.strip() == "":
            return {
                "valid" : False,
                "msg" : "Please provide the user_id to continue."
            }

        self.cursor.execute("SELECT address.address_id, address.address_fullname, address.address_phone_number, address.address_line1, address.address_line2, address.address_city, address.address_postcode, address.address_status, address.address_updated_on, address.address_created_on, state.state_name AS address_state FROM address LEFT JOIN state ON state.state_id = address.address_state WHERE address.address_user_id = '{}'".format(user_id))
        addresses = self.cursor.fetchall()

        if len(addresses) > 0:
            for address in addresses:
                address['address_created_on'] = str(address['address_created_on'])
                if address['address_updated_on'] != None:
                    address['address_updated_on'] = str(address['address_updated_on'])
            return {
                'valid': True,
                "addresses": addresses
            }
        return {
            "valid": False,
            "addresses": []
        }