from . import auth
from flask import jsonify
from app.models.user import User
from .. import db, request


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
            user = User(user_id=email)
            user.password = password
            db.session.add(user)
            db.session.commit()
            return jsonify(message=f'User ${email} created successfully'), 201
        else:
            return jsonify(message='Passwords don\'t match'), 409

