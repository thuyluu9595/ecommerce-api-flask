from . import api
from .models.users import User
from flask import jsonify
from flask import json
from bson.json_util import dumps


@api.route("/user")
def home():
    user = User.find_one({"name": "Thuy"},{"password": 0})
    return user.json(), 200
