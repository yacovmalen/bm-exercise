from flask import request
from flask_restful import abort
from pymongo import MongoClient


def is_authenticated(f):
    """Checks whether user's api is valid or raises error 401."""

    def decorator(*args, **kwargs):
        if 'SECURITY_TOKEN_AUTHENTICATION_KEY' not in request.headers or not is_token(request.headers['SECURITY_TOKEN_AUTHENTICATION_KEY']):
            abort(401)
        return f(*args, **kwargs)

    return decorator


def is_token(token):
    client = MongoClient('localhost', 27017)
    response = client['school']['users'].find({'api_token': token})
    allow_access = len([res['api_token'] for res in response]) > 0
    client.close()
    return allow_access
