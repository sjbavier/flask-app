from . import auth
from flask import jsonify
from app.models.user import User, Role
from app import jwt_required, get_jwt_identity
from .. import db, request, create_access_token
import os


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
            if email == os.getenv('SERVER_ADMIN'):
                user.add_role('Admin')
            else:
                user.add_role('User')
            db.session.add(user)
            db.session.commit()
            return jsonify(message=f'User {email} created successfully'), 201
        else:
            return jsonify(message='Passwords don\'t match'), 409


@auth.route('/login', methods=['POST'])
def login():
    email = ''
    password = ''
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test_email = User.query.filter_by(user_id=email).first()
    if test_email:
        user = User.query.filter_by(user_id=email).first()
        verified_password = user.verify_password(password)
        if verified_password:
            role_id = user.role_id
            role = Role.query.filter_by(id=role_id).first()
            access_token = create_access_token(identity=user.id)
            payload = {
                'userId': user.user_id,
                'role': role.name,
                'access_token': access_token,
                'message': 'Login Successful'
            }

            return jsonify(payload)
        else:
            return jsonify(message='Password is incorrect'), 409

    return jsonify(message='User does not exist'), 404


@auth.route('/authorize', methods=['GET'])
@jwt_required()
def authorize():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    role_id = user.role_id
    role = Role.query.filter_by(id=role_id).first()
    payload = {
        'userId': user_id,
        'role': role.name
    }
    return jsonify(payload)