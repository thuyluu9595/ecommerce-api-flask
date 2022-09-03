from datetime import datetime
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from bson import ObjectId
from flask import json


def admin_validator():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claim = get_jwt()
            is_admin = claim['isAdmin']
            if not is_admin:
                return {'error': {'message': 'Admin is required'}}, 401
            return fn(*args, **kwargs)
        return decorator
    return wrapper


# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, arg):
#         if isinstance(arg, datetime):
#             return arg.isoformat()
#         elif isinstance(arg, ObjectId):
#             return str(arg)
#         else:
#             super().default(self, arg)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
