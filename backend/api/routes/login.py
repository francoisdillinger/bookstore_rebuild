from flask import Blueprint, request, session, jsonify
from ..models import User, db
from werkzeug.security import check_password_hash
# from flask_session import Session
# from .. import server_session

login = Blueprint('login', __name__)
# server_session = Session(app)

@login.route('/login', methods=['POST'])
def log_in():
    email = request.json['email']
    password = request.json['password']
    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        if check_password_hash(user_exists.password, password):
            session["user_id"] = user_exists.id
            return {"success":"Successfully logged in."}
        else:
            return {"error": "Please try logging in again."}, 401
    return {"error":"Please try again."}, 401


@login.route('/login/user', methods=["GET"])
def logged_in():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "User not logged in."}
    else:
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password
    }), 200