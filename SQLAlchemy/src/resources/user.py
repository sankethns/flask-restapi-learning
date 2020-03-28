import sqlite3

from flask import request
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help="Username is required",
                           required=True)
        parser.add_argument('password', type=str, help="Password is required",
                           required=True)
        data = parser.parse_args()
        if UserModel.get_by_username(data['username']):
            return {"message" : "username %s already exists" % \
                        (data['username']) }, 401

        user = UserModel(**data)
        user.add_to_db()

        return {"message" : "user registered"}, 201
