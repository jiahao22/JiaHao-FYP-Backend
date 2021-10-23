from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Import the Users class
from user.auth.functions import UserCheckAccountExists, UserLogin, UserRegister

app = Flask(__name__)

# Secret Key for generate the access token
app.secret_key = 'ecommerce'

# config JWT to expire within 3 days
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

api = Api(app)
jwt = JWTManager(app)

CORS(app)

api_url = '/api/'

# Users Module Start
api.add_resource(UserCheckAccountExists, api_url + '/user/auth/check')
api.add_resource(UserLogin, api_url + '/user/auth/login')
api.add_resource(UserRegister, api_url + '/user/auth/register')
# Users Module End

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
