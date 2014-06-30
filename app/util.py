#!bin/python

from functools import wraps
from flask import g, abort

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if ((not g.user) or (g.user.role < 10)):
            abort(404)

        return func(*args, **kwargs)

    return decorated_function