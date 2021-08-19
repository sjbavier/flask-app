from . import auth
from flask import jsonify
from app.models.user import User
from .. import db, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


@auth.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test_email = User.query.filter_by(user_id=email).first()
    if test_email:
        return jsonify(message='Email already exists'), 409
    else:
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            user = User(user_id=email, password=password)
            # TODO : Add role to default user
            db.session.add(user)
            db.session.commit()
            return jsonify(message=f'User ${email} created successfully'), 201
        else:
            return jsonify(message='Passwords don\'t match'), 409


@auth.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test_email = User.query.filter_by(user_id=email).first()
    if test_email:
        user = User(user_id=email)
        verified_password = user.verify_password(password)
        if verified_password:
            access_token = create_access_token(identity=email)
            return jsonify(message='Login successful', access_token=access_token)
        else:
            return jsonify(message='Password is incorrect'), 409

