import certifi
from flask import Flask
from config import config
# from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient


# Connect database
ca = certifi.where()
load_dotenv(find_dotenv())
password = os.environ.get("MONGO_PWD")
connection_string = f'mongodb+srv://thuyluu9595:{password}@ecommerce.tmleeao.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string, tlsCAFile=ca)
db = client.test


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
