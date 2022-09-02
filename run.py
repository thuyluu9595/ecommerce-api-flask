import os
from app import create_app
# from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User)


# @app.before_first_request
# def create_tables():
#     db.create_all()

