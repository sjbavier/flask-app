from functools import wraps
from flask import abort
from app import get_jwt_identity
from app.models.user import Permission
from app.models.user import User


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_email = get_jwt_identity()
            current_user = User.query.filter_by(user_id=current_email).first()
            print(current_user.role)
            if not current_user.can(permission):
                abort(403)
            func = f(*args, **kwargs)
            return func
        return decorated_function
    return decorator


def execute_required(f):
    return permission_required(Permission.EXECUTE)(f)


def debug(func):
    """Print the function signature and return value"""

    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug
