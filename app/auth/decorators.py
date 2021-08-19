from functools import wraps
from flask import abort


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
