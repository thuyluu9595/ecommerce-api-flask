from datetime import datetime
from bson import ObjectId
from flask import json


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
