from . import api
from .models.users import User
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from app.middleware import admin_validator

parser = reqparse.RequestParser()
parser.add_argument('email',
                    type=str,
                    required=True,
                    help="This field cannot be empty")

parser.add_argument('password',
                    type=str,
                    required=True,
                    help="Password cannot be blank")


class UserAction(Resource):
    @jwt_required()
    def get(self, _id):
        """
        get User by id
        :param _id:
        :return:
        """
        try:
            user_id = ObjectId(_id)
        except Exception as e:
            return {"message": "Invalid id"}, 401

        user = User.find_one({"_id": user_id}, {"password": 0})
        if user:
            return user, 200
        return {"message": "Invalid token"}, 401

    @admin_validator()
    def put(self, _id):
        try:
            user_id = ObjectId(_id)
        except Exception as e:
            return {'message': 'Invalid id'}, 401

        user = User.find_one({"_id": user_id}, {"password": 0})
        if user:
            _parser = reqparse.RequestParser()
            _parser.add_argument('email',
                                 type=str,
                                 required=True)

            _parser.add_argument('name',
                                 type=str,
                                 required=True)
            _parser.add_argument('isAdmin',
                                 type=bool,
                                 required=True)
            data = _parser.parse_args()
            print(data['isAdmin'])
            User.update_one(user, {
                '$set': {'name': data['name'],
                         'email': data['email'],
                         'isAdmin': data['isAdmin']
                         }
            })
            return {}, 200
        else:
            return {'message': 'User doesn''t exist'}, 401

    @admin_validator()
    def delete(self, _id):
        try:
            user_id = ObjectId(_id)
        except Exception as e:
            return {'message': 'Invalid id'}, 401

        user = User.find_one({'_id': user_id})
        if user:
            User.delete_one(user)
            return 200
        else:
            return {'message': 'User doesn''t exist'}, 401


class UserSignin(Resource):
    @classmethod
    def post(cls):
        data = parser.parse_args()
        user = User.find_one({"email": data.email})

        if user and data.password == user['password']:
            access_token = create_access_token(identity=str(user['_id']), fresh=True,
                                               additional_claims={"isAdmin": user['isAdmin']})
            refesh_token = create_refresh_token(str(user['_id']))
            return {
                       '_id': user['_id'],
                       'name': user['name'],
                       'email': user['email'],
                       'isAdmin': False,
                       'token': access_token,
                       'refesh_token': refesh_token
                   }, 200
        return {'message': 'Invalid credentials'}, 401


class UserRegister(Resource):
    @classmethod
    def post(self):
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="Password cannot be blank")
        data = parser.parse_args()
        if User.find_one({"email": data.email}):
            return {"error": {"message": "string"}}, 500
        user = {
            "name": data.name,
            "email": data.email,
            "password": data.password,
            "isAdmin": False
        }
        user_id = User.insert_one(user).inserted_id
        user.pop('password')
        user['_id'] = str(user_id)
        user['token'] = create_access_token(identity=str(user_id), fresh=True)
        return user, 200


class UserList(Resource):
    @admin_validator()
    def get(self):
        users = User.find()
        mylist = []
        for user in users:
            user['_id'] = str(user['_id'])
            mylist.append(user)
        return mylist, 200
