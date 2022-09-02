from bson.json_util import dumps
from flask_restful import Resource
from app.api.models.users import User


class Usr(Resource):
    def get(self):
        user = User.find_one({"name": "Thuy"}, {"password": 0})
        return user, 200
