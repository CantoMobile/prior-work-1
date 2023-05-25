from flask import request, jsonify, url_for
from functools import wraps
from .auth_service import AuthService
from repositories.user_repository import UserRepository

user_repo = UserRepository()

auth = AuthService()

# MIDDLEWARE


def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        print(token)
        email = auth.verify_auth_token(token)
        validation = validate_permissions(email)
        if not validation:
            return jsonify({"error": "You not have permission to make this request"}), 401
        return f(*args, **kwargs)
    return decorator


def validate_permissions(email):
    resource = extract_segment(request.url, 3)
    method = request.method
    result = user_repo.verify_permissions(email, resource, method)
    return result 


def extract_segment(url, segment_index):
    segments = url.split('/')
    if len(segments) > segment_index:
        return segments[segment_index]
    return None
