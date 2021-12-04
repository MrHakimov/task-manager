import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .db_all import init_db

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PG_DSN')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

init_db(SQLAlchemy(app))

from controllers import init_controllers
init_controllers(app)


def get_app():
    return app
