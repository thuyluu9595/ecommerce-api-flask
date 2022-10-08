import os
from app.middleware import JSONEncoder
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ##
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    RESTFUL_JSON = {'cls': JSONEncoder}
    JWT_SECRET_KEY = 'abcdef123'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
