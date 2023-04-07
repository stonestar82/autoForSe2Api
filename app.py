from flask import Flask, g
from functools import wraps
from flask_restful import Resource, Api
from flask_restful import reqparse
from src.controller.Auth import *
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
api = Api(app)


api.add_resource(AuthLogin, '/login')
api.add_resource(Auth, "/auth")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)