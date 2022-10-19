from flask import request, Blueprint, jsonify
from ..models import User, db
from werkzeug.security import generate_password_hash

register = Blueprint('register', __name__)

def format_data(user):
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password
    }), 200

@register.route('/register', methods=['POST'])
def users():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password1 = request.json['password1']
    password2 = request.json['password2']
    
    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        return {"error":"User already exists."}, 409
    elif len(first_name) <= 2:
        return {"error":"First name must be greater than 2 characters."}, 400
    elif len(last_name) <= 2:
        return {"error":"Last name must be greater than 2 characters."}, 400
    elif len(email) <= 4:
        return {"error":"Email must be greater than 4 characters."}, 400
    elif password1 != password2:
        return {"error":"Passwords don't match."}, 400
    elif len(password1) < 7:
        return {"error":"Password must be at least 7 characters."}, 400
    else:
        password1 = generate_password_hash(request.json['password1'], method="sha256")
        user = User(first_name = first_name, last_name = last_name, email = email, password = password1)
        db.session.add(user)
        db.session.commit()
        print(f'User with following data: {first_name}, {last_name}, {email}, {password1}')
        return format_data(user)