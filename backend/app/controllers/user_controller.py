from flask import Blueprint, request, url_for
from app.services.middleware import validate_token
from app.services.user_service import *
from app.services.reviews_service import reviews_by_user
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.config.database import Database
from app.utils.logger import logger



category_repo = CategoryRepository()
user_repo = UserRepository()

user_bp = Blueprint('user_bp', __name__,  url_prefix='/users')


@user_bp.route('', methods=['GET', 'POST'])
# @validate_token
def users():
    if request.method == 'GET':
        return get_all_users()

    elif request.method == 'POST':
        data = request.json
        return get_all_users(data['page'])


@user_bp.route('/add_user', methods=['POST'])
# @validate_token
def add_user():
    return create_user()


@user_bp.route('/register', methods=['POST'])
def user_registry():
    return create_user(None,True)


@user_bp.route('/<user_id>', methods=['GET', 'PUT', 'DELETE'])
# @validate_token
def user(user_id):
    if request.method == 'GET':
        return get_one_user(user_id)

    elif request.method == 'PUT':
        return update_one_user(user_id)

    elif request.method == 'DELETE':
        return delete_one_user(user_id)


@user_bp.route('/authentication', methods=['POST'])
def authentication():
    return user_authentication()


@user_bp.route('/set_password', methods=['POST'])
def set_password():
    return set_user_password()


@user_bp.route('/<user_id>/add_role/<role_id>', methods=['PUT'])
@validate_token
def add_role(user_id, role_id):
    return add_user_role(user_id, role_id)


@user_bp.route('/<user_id>/remove_role/<role_id>', methods=['PUT'])
@validate_token
def remove_role(user_id, role_id):
    return remove_user_role(user_id, role_id)


@user_bp.route('/<user_id>/reviews', methods=['GET'])
@validate_token
def site_reviews(user_id):
    return reviews_by_user(user_id)


@user_bp.route('/<user_id>/save_site/<site_id>', methods=['PUT'])
@validate_token
def save_site(user_id, site_id):
    return save_site_user(user_id, site_id)


@user_bp.route('/<user_id>/information', methods=['PUT'])
def update_information(user_id):
    return update_user_information(user_id)


@user_bp.route('/validate_otp', methods=['POST'])
def validate_otp():
    return validate_user_otp()

@user_bp.route('/<user_id>/remove_site/<site_id>', methods=['DELETE'])
# @validate_token
def remove_site(user_id, site_id):
    return remove_site_user(user_id, site_id)


# google = oauth.register(
#     name='google',
#     client_id='YOUR_GOOGLE_CLIENT_ID',
#     client_secret='YOUR_GOOGLE_CLIENT_SECRET',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     authorize_prompt=None,
#     authorize_response=None,
#     token_url='https://accounts.google.com/o/oauth2/token',
#     token_params=None,
#     refresh_token_url=None,
#     client_kwargs={'scope': 'openid profile email'},
# )

# @app.route('/auth/google')
# def google_login():
#     return google.authorize_redirect(url_for('google_auth', _external=True))

# @app.route('/auth/google/callback')
# def google_auth():
#     try:
#         token = google.authorize_access_token()
#         user_info = google.parse_id_token(token)
#         # Store user_info in session or database as needed
#         return 'Google login successful!'
#     except OAuthError as e:
#         # Handle authentication error
#         return str(e)
