from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_validator():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claim = get_jwt()
            is_admin = claim['isAdmin']
            if not is_admin:
                return {'error': {'message': 'Admin is required'}}, 401
            return fn(*args, **kwargs)

        return decorator

    return wrapper
