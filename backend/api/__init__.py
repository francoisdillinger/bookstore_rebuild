from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://admin:password@localhost/bookstore_rebuild'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.register import register
    app.register_blueprint(register)

    return app

# class User(db.Model):
#     __tablename__ = 'Users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(200), nullable=False, unique=False)
#     last_name = db.Column(db.String(200), nullable=False, unique=False)
#     email = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(150), nullable =False, unique=False)

# db.create_all()
# def create_DB(app, User, Book):
#     with app.app_context():
#         if not path.exists('bookstore/' + DB_NAME):
#             db.create_all(app=app)
#             add_admin_user_to_db(User)
#             # add_initial_book_data(Book)

# def add_admin_user_to_db(User):
#     print('Creating user: Admin')
#     user = User(
#         first_name='admin', 
#         last_name='admin', 
#         email='admin1@gmail.com', 
#         password=generate_password_hash('1234567', method='sha256'), 
#         admin_status=True
#     )
    
#     db.session.add(user)
#     db.session.commit()

