import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required = True, help = "This field cannot be left empty")
    parser.add_argument('password', type = str, required = True, help = "This field cannot be left empty")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {"message":"user with the name '{}' already exists".format(data['username'])}, 400
        user = UserModel(data['username'], data['password'])
        #Can be replaced by user = UserModel(**data)
        user.save_to_db()

        return {"message":"User created successfully"}, 201
