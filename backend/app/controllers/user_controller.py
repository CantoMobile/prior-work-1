from flask import Blueprint, request, jsonify, abort
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.reviews_repository import ReviewsRepository
from app.services.auth_service import AuthService
from app.services.user_site_service import create_relationship
from app.services.middleware import validate_token
from app.services.user_service import *

role_repo = RoleRepository()
user_repo = UserRepository()
reviews_repo = ReviewsRepository()
auth = AuthService()

user_bp = Blueprint('user_bp', __name__,  url_prefix='/users')


@user_bp.route('', methods=['GET', 'POST'])
@validate_token
def users():
    if request.method == 'GET':
        users_data = user_repo.findAll()
        return users_data

    elif request.method == 'POST':
        data = request.json
        errors = validate_email_domain(data['email'])
        if errors[0] == False:
            return {"error": errors[1]}, 401

        user = User(
            name=data['name'],
            email=data['email'],
            password=auth.encrypt(data['password'])
        )
        user_data = user_repo.save(user)
        create_relationship(user_data['_id'])
        return jsonify(user_data)


@user_bp.route('/register', methods=['POST'])
def user_registry():
    data = request.json
    errors = validate_email_domain(data['email'])
    if errors[0] == False:
        return {"error": errors[1]}, 401

    user = User(
        name=data['name'],
        email=data['email'],
        password=auth.encrypt(data['password'])
    )
    user_data = user_repo.save(user)
    role_id = "646c0099d72ed166e49c3890"
    role_data = role_repo.findById(role_id)
    user_data['role'] = {'collection': 'role', '_id': role_data['_id']}
    user_repo.update(user_data['_id'], user_data)
    create_relationship(user_data['_id'])
    return auth.generate_auth_token(user_data, role_id)


@user_bp.route('/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
@validate_token
def user(user_id):
    user_data = user_repo.findById(user_id)
    if not user_data:
        abort(404)

    if request.method == 'GET':
        return user_data

    elif request.method == 'PUT':
        data = request.json
        if 'name' in data:
            user_data['name'] = data['name']
        if 'email' in data:
            user_data['email'] = data['email']
        if 'password' in data and user_data['password'] != data['password']:
            user_data['password'] = auth.encrypt(data['password'])
        if 'role' in data:
            user_data['role'] = data['roles']
        return user_repo.update(user_id, user_data)

    elif request.method == 'DELETE':
        user_repo.delete(user_id)
        return jsonify({'message': 'User deleted'})


@user_bp.route('/authentication', methods=['POST'])
def authentication():
    data = request.json
    user_data = user_repo.find_by_email(data['email'])
    if not user_data:
        abort(404)
    user = User(**user_data)
    role_id = user_data['role']['_id']
    if user.verify_password(auth.encrypt(data['password'])):
        return auth.generate_auth_token(user_data, role_id)
    else:
        return jsonify({'message': 'Password is incorrect'}), 401


@user_bp.route('/<string:user_id>/set_password', methods=['PUT'])
@validate_token
def set_user_password(user_id):
    data = request.json
    user_data = user_repo.findById(user_id)
    user_data.pop('_id')
    if not user_data:
        abort(404)

    user = User(**user_data)
    response = user.set_password(auth.encrypt(data['password']))
    if response != None and response == True:
        update = user_repo.update(user_id, user)
        return jsonify(update)
    else:
        return {"error": "Failed to update password"}, 304


@user_bp.route('/<user_id>/add_role/<role_id>', methods=['PUT'])
@validate_token
def add_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    role_data = role_repo.findById(role_id)
    if not user_data or not role_data:
        abort(404)

    # validation = any(role_item['_id'] == role_id for role_item in user.roles)
    if user_data['role'] != None:
        if role_id in user_data['role']['_id']:
            return {'Error': 'The user already has the role assigned'}, 304
    else:
        user_data['role'] = {'collection': 'role', '_id': role_data['_id']}
        return user_repo.update(user_id, user_data)


@user_bp.route('/<user_id>/remove_role/<role_id>', methods=['PUT'])
@validate_token
def remove_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    role_data = role_repo.findById(role_id)

    if not user_data or not role_data:
        abort(404)
    # validation = any(role_item['_id'] == role_id for role_item in user.roles)
    if user_data['role'] != None:
        if role_id in user_data['role']['_id']:
            # if validation:
            user_data['role'] = None
            return user_repo.update(user_id, user_data)
    else:
        return jsonify({"Error": "This role is not associated with this user"}), 304
    

@user_bp.route('/<user_id>/reviews', methods=['GET', 'PUT', 'DELETE'])
@validate_token
def site_reviews(user_id):
    try:
        reviews = reviews_repo.findAllByField('user_id', user_id)

        return jsonify(reviews)
    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
