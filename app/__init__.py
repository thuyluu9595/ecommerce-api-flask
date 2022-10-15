import os
import certifi
from flask import Flask
from config import config
# from app.middleware import JSONEncoder
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from flask_restful import Api
from flask_jwt_extended import JWTManager

load_dotenv(find_dotenv())
ca = certifi.where()

# Connecting Database
password = os.environ.get("MONGO_PWD")
connection_string = os.environ.get('CONNECTION_STR')
client = MongoClient(connection_string, tlsCAFile=ca)
db = client.test


def create_app(config_name='default'):
    app = Flask(__name__)
    # app.config['PROPAGATE_EXCEPTIONS'] = True
    # app.config['RESTFUL_JSON'] = {'cls': JSONEncoder}
    # app.config['JWT_SECRET_KEY'] = 'abcdef123'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api = Api(app, prefix='/api')
    jwt = JWTManager(app)

    from .api import users, products, orders, reviews, upload
    # --------------> User routes <--------------------------------
    api.add_resource(users.UserUpdateProfile, '/users/profile')
    api.add_resource(users.UserAction, '/users/<string:_id>')
    api.add_resource(users.UserSignin, '/users/signin')
    api.add_resource(users.UserRegister, '/users/register')
    api.add_resource(users.UserList, '/users')
    # --------------> Product routes <--------------------------------
    api.add_resource(products.Products, '/products')
    api.add_resource(products.ProductActions, '/products/<string:_id>')
    api.add_resource(products.ProductCategory, '/products/categories')
    api.add_resource(products.ProductBrands, '/products/brands')
    # --------------> Order routes <--------------------------------
    api.add_resource(orders.OrderConvention, '/orders')
    api.add_resource(orders.OrderActions, '/orders/<string:_id>')
    api.add_resource(orders.OrderSummary, '/orders/summary')
    api.add_resource(orders.GetUserOrder, '/orders/mine')
    api.add_resource(orders.GetOrderById, '/orders/user/<string:_id>')
    api.add_resource(orders.DeliverOrder, '/<string:_id>/deliver')
    api.add_resource(orders.OrderCancellation, '/<string:_id>/cancelrequest')
    api.add_resource(orders.ConfirmCancellation, '/<string:_id>/canceled')
    # --------------> Review routes <--------------------------------
    api.add_resource(reviews.UserReview, '/reviews/user')
    api.add_resource(reviews.ProductReview, '/reviews/product/<string:_id>')
    api.add_resource(reviews.UserReviewForAdmin, '/reviews/user/<string:_id>')
    api.add_resource(reviews.ReviewActions, '/reviews/<string:_id>')
    # --------------> Upload routes <--------------------------------
    api.add_resource(upload.Upload, '/uploads/s3')

    return app
