from .. import db
from .. import ma
import os
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    roles_collection = db.relationship('Role', secondary='user_role', back_populates='users_collection', lazy='joined', join_depth=1)

    def __repr__(self):
        return '<User %r>' % self.user_password

    # TODO: fix the role permissions and verification
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.roles_collection or self.roles_collection is None:
            if self.user_id == os.getenv('SERVER_ADMIN'):
                self.roles_collection = Role.query.filter_by(name="Admin").first()
            else:
                # self.roles_collection = Role.query.filter_by(default=True).first()
                self.roles_collection.append(Role.query.filter_by(default=True).first())

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

    # def can(self, perm):
    #     return self.role is not None and self.role.has_permission(perm)


class UserSchema(ma.Schema):
    id = fields.Integer()
    user_id = fields.String()
    user_password = fields.String()
    roles_collection = fields.Nested(lambda: RoleSchema(only=('id', 'name',)), many=True)


class Permission:
    READ = 1
    WRITE = 2
    EXECUTE = 4


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users_collection = db.relationship('User', secondary='user_role', back_populates='roles_collection', lazy='joined', join_depth=1)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        """
        finds existing roles, so that changes to permissions or roles can be made.
        """

        roles = {
            'User': [Permission.READ],
            'Editor': [Permission.READ, Permission.WRITE],
            'Admin': [Permission.READ, Permission.WRITE, Permission.EXECUTE]
        }
        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class RoleSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    default = fields.Boolean()
    permissions = fields.Integer()
    users_collection = fields.Nested(lambda: UserSchema(only=('id', 'user_id')), many=True)


class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    def __repr__(self):
        return '<UserRole %r>' % self.name
