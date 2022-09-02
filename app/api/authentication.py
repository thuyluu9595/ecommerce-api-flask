# from flask import g, jsonify
# from flask_httpauth import HTTPBasicAuth
# from ..models import User
# from . import api
# auth = HTTPBasicAuth()
#
#
# @auth.verify_password
# def verify_password(username, password):
#     if username == '':
#         return False
#     user = User.query.filter_by(user_name = username).first()
#     if not user:
#         return False
#     g.current_user = user
#     return user.verify_password(password)