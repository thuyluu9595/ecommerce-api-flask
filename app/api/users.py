import os
from .models.user import User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from .decorators import admin_validator
from dotenv import load_dotenv, find_dotenv
import bcrypt

load_dotenv(find_dotenv())

_parser = reqparse.RequestParser()
_parser.add_argument('email',
                     type=str,
                     required=True,
                     help="This field cannot be empty")
_parser.add_argument('password',
                     type=str,
                     required=True,
                     help="Password cannot be blank")


# /api/users/<string:_id>
class UserAction(Resource):
    @jwt_required()
    def get(self, _id):
        """
        get User by id
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
            __parser = reqparse.RequestParser()
            __parser.add_argument('email',
                                 type=str,
                                 required=True)

            __parser.add_argument('name',
                                 type=str,
                                 required=True)
            __parser.add_argument('isAdmin',
                                 type=bool,
                                 required=True)
            data = __parser.parse_args()
            # print(data['isAdmin'])
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


# /api/users/signin
class UserSignin(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = User.find_one({"email": data.email})

        if user and bcrypt.checkpw(data.password.encode('utf-8'), user['password'].encode('utf-8')):
            access_token = create_access_token(identity=str(user['_id']), fresh=True,
                                               additional_claims={"isAdmin": user['isAdmin']})
            refresh_token = create_refresh_token(str(user['_id']))
            return {
                       '_id': user['_id'],
                       'name': user['name'],
                       'email': user['email'],
                       'isAdmin': user['isAdmin'],
                       'token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'message': 'Invalid credentials'}, 401


# /api/users/register
class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_register_parser = reqparse.RequestParser()
        user_register_parser.add_argument('email', type=str, required=True, help="This field cannot be empty")
        user_register_parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        user_register_parser.add_argument('name', type=str, required=True,help="Name cannot be blank")

        data = user_register_parser.parse_args()

        admin_email = os.environ.get('ADMIN_EMAIL')
        isAdmin = data.email == admin_email

        if User.find_one({"email": data.email}):
            return {"error": {"message": "email is already used"}}, 500
        user = {
            "name": data.name,
            "email": data.email,
            "password": bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "isAdmin": isAdmin
        }
        user_id = User.insert_one(user).inserted_id
        user.pop('password')
        user['_id'] = str(user_id)
        user['token'] = create_access_token(identity=str(user_id), fresh=True)
        return user, 200


# /api/users
class UserList(Resource):
    @admin_validator()
    def get(self):
        users = User.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return user_list, 200


# /api/users/profile
class UserUpdateProfile(Resource):
    @jwt_required()
    def put(self):
        user_update_parser = reqparse.RequestParser()
        user_update_parser.add_argument('email', type=str, required=True, help="This field cannot be empty")
        user_update_parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        user_update_parser.add_argument('name', type=str, required=True,help="Name cannot be blank")

        data = _parser.parse_args()
        user_id = ObjectId(get_jwt_identity())
        user = User.find_one({'_id': user_id})
        if user:
            token = create_access_token(identity=str(user_id), fresh=True)
            User.update_one(user, {
                '$set': {
                    'name': data.name,
                    'email': data.email,
                    'password': bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                }
            })
            return {
                       '_id': str(user['_id']),
                       'name': user['name'],
                       'email': user['email'],
                       'isAdmin': user['isAdmin'],
                       'token': token
                   }, 200
        else:
            return {{'message': 'Invalid user'}}, 401
