from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    """
    the roles.id argument for ForeignKey should be interpreted as id values from roles table
    """
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        """
        returns boolean value for password verification
        """
        return check_password_hash(self.user_password, password)



