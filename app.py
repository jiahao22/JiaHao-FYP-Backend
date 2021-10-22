from flask import Flask, jsonify
from flask_restful import Api
from flask_restful import Resource, reqparse

app = Flask(__name__)

api = Api(app)


class Test(Resource):

    def post(self):
        return "Hi"


api.add_resource(Test, '/test')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
