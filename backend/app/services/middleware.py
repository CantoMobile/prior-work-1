import re
from bson import ObjectId
from flask import request, jsonify
from functools import wraps

from app.utils.logger import logger
from .auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.site_repository import SiteRepository
from urllib.parse import urlsplit

user_repo = UserRepository()
site_repo = SiteRepository()

auth = AuthService()

# MIDDLEWARE


def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        result = auth.verify_auth_token(token)
        if type(result) is dict:
            return result, 401
        validation = validate_permissions(result[0], result[1])
        if not validation:
            logger.error("This user has not permission to access this page: " + request.url)
            return jsonify({"error": "You not have permission to make this request"}), 401
        return f(*args, **kwargs)
    return decorator


def validate_permissions(email, permissions):
    resource = extract_segment(request.url)
    method = request.method

    if permissions != None:
        if (resource, method) in permissions:
            return True
        else: 
            return False
    else: 
        return False
    #return result


def extract_segment(url):
    segments = delete_url(url)
    if len(segments) > 0:
        result = "/".join(segments)
        if len(segments) > 1:
            try:
                [ObjectId(segment) for segment in segments]
                result = "?"
            except:
                pass
        return result
    return None


def delete_url(url):
    parsed_url = urlsplit(url)
    complete_route = parsed_url.path.rstrip('/')
    if parsed_url.query:
        complete_route += parsed_url.query
    if parsed_url.fragment:
        complete_route += parsed_url.fragment
    segments = [segment for segment in complete_route.split('/') if segment]
    segments = ["?" if re.match(r'^[0-9a-fA-F]{24}$', segment) else segment for segment in segments]
    return segments


def verify_admin(user_id, site_id):
    site = site_repo.findById(site_id)
    user = user_repo.findById(user_id)

    if (site):
        admin_email = site['admin_email']
        user_email = user['email']

        return admin_email == user_email
    
    return False


def admin_permission_required(f):
    def decorator(*args, **kwargs):
        user_id = kwargs.get('user_id')# get_user_id_from_token()  # Replace with your implementation to get the user ID from the token
        site_id = kwargs.get('site_id')  # Modify this based on the actual parameter name in your route

        if not verify_admin(user_id, site_id):
            return jsonify({"error": "You do not have permission to perform this action"}), 401

        return f(*args, **kwargs)

    return decorator