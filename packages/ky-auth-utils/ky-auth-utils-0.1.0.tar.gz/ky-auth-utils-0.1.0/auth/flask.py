from functools import wraps
from flask import request, g, abort
from auth import Auth


def auth_required(f):
    """Checks whether user is logged in or raises error 401."""

    @wraps(f)
    def decorator(*args, **kwargs):
        g.auth = Auth.from_dict(request.headers)
        if not g.auth.is_login():
            abort(401)
        return f(*args, **kwargs)

    return decorator


def auth_optional(f):
    """Get auth info from headers."""

    @wraps(f)
    def decorator(*args, **kwargs):
        g.auth = Auth.from_dict(request.headers)
        return f(*args, **kwargs)

    return decorator


def role_required(role):
    """Checks whether user has role raises error 403."""

    def inner_wrap(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if 'auth' not in g:
                g.auth = Auth.from_dict(request.headers)
            if not g.auth.has_role(role):
                abort(403)
            return f(*args, **kwargs)

        return decorator
    return inner_wrap
