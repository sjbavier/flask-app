from .. import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_password = db.Column(db.String(64), nullable=False)
    roles = db.Column(db.Enum, nullable=False)

    """
    the roles.id argument for ForeignKey should be interpreted as id values from roles table
    """
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.user_password
