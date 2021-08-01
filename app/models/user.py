from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary='user_role')

    def __repr__(self):
        return '<User %r>' % self.user_password

    @property
    def password(self):
        """
        write only property
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password, method='pbkdf2:sha512', salt_length=32)

    def verify_password(self, password):
        """
        returns boolean value for password verification
        """
        return check_password_hash(self.user_password, password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', secondary='user_role')

    def __repr__(self):
        return '<Role %r>' % self.name


class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    def __repr__(self):
        return '<UserRole %r>' % self.name
