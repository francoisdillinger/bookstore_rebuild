from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from .database import check_and_create_database
import redis
from flask_session import Session

db = SQLAlchemy()
server_session = Session()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this_was_a_major_pain'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://admin:password@localhost/bookstore_rebuild'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')


    from .routes.register import register
    from .routes.login import login
    
    app.register_blueprint(register)
    app.register_blueprint(login)

    
    server_session.init_app(app)
    db.init_app(app=app)
    check_and_create_database(app, db)

    return app

