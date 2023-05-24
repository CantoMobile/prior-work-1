from flask import request, jsonify
from functools import wraps
from .auth_service import AuthService

auth = AuthService()

# MIDDLEWARE


def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        print(token)
        auth.verify_auth_token(token)
        return f(*args, **kwargs)
    return decorator
