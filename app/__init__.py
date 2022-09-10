import certifi
from flask import Flask
from config import config
from app.middleware import JSONEncoder
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from app.usr import Usr


# Connect database
ca = certifi.where()
load_dotenv(find_dotenv())
password = os.environ.get("MONGO_PWD")
connection_string = f'mongodb+srv://thuyluu9595:{password}@ecommerce.tmleeao.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string, tlsCAFile=ca)
db = client.test


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['RESTFUL_JSON'] = {'cls': JSONEncoder}
    app.config['JWT_SECRET_KEY'] = 'abcdef123'
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    api = Api(app)
    jwt = JWTManager(app)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    from .api import users, products
    # api.add_resource(Usr, '/usr')
    # --------------> User routes <--------------------------------
    api.add_resource(users.UserUpdateProfile, '/api/users/profile')
    api.add_resource(users.UserAction, '/api/users/<string:_id>')
    api.add_resource(users.UserSignin, '/api/users/signin')
    api.add_resource(users.UserRegister, '/api/users/register')
    api.add_resource(users.UserList, '/api/users')
    # --------------> Product routes <--------------------------------
    api.add_resource(products.Products, '/api/products')
    api.add_resource(products.ProductActions, '/api/products/<string:_id>')
    api.add_resource(products.ProductCategory, '/api/products/categories')
    api.add_resource(products.ProductBrands, '/api/products/brands')
    return app
