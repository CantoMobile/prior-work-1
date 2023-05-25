from flask import request, jsonify, abort
from models.role_model import Role
from models.user_model import User
from . import user_bp
from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
from services.auth_service import AuthService
from services.middleware import validate_token
role_repo = RoleRepository()
user_repo = UserRepository()
auth = AuthService()


@user_bp.route('/users', methods=['GET', 'POST'])
@validate_token
def users():
    if request.method == 'GET':
        users_data = user_repo.findAll()
        return users_data

    elif request.method == 'POST':
        data = request.json
        roles = data.pop('roles', [])  # extract roles from data
        user = User(
            name=data['name'],
            email=data['email'],
            password=auth.encrypt(data['password']),
            roles=roles
        )
        user_data = user_repo.save(user)
        return jsonify(user_data)


@user_bp.route('/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
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
        if 'roles' in data:
            user_data['roles'] = data['roles']
        return user_repo.update(user_id, user_data)

    elif request.method == 'DELETE':
        user_repo.delete(user_id)
        return jsonify({'message': 'User deleted'})


@user_bp.route('/users/authentication', methods=['POST'])
def authentication():
    data = request.json
    print(data)
    user_data = user_repo.find_by_email(data['email'])
    if not user_data:
        abort(404)

    user = User(**user_data)

    if user.verify_password(auth.encrypt(data['password'])):
        return auth.generate_auth_token(data)
    else:
        return jsonify({'message': 'Password is incorrect'}), 401


@user_bp.route('/users/<string:user_id>/set_password', methods=['PUT'])
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
        print("update:", update)
        return jsonify(update)
    else:
        return {"error": "Failed to update password"}, 304


@user_bp.route('/users/<user_id>/add_role/<role_id>', methods=['PUT'])
@validate_token
def add_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    role_data = role_repo.findById(role_id)
    if not user_data or not role_data:
        abort(404)

    user = User(**user_data)
    role = Role(**role_data)

    validation = any(role_item['_id'] == role_id for role_item in user.roles)
    if validation:
        return {'Error': 'The user already has the role assigned'}, 304
    else:
        return user_repo.updateArray(user_id, 'roles', role)


@user_bp.route('/users/<user_id>/remove_role/<role_id>', methods=['PUT'])
@validate_token
def remove_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    role_data = role_repo.findById(role_id)

    if not user_data or not role_data:
        abort(404)

    user = User(**user_data)
    role = Role(**role_data)

    validation = any(role_item['_id'] == role_id for role_item in user.roles)
    if validation:
        return user_repo.deleteFromArray(user_id, 'roles', role)
    else:
        return jsonify({"Error": "This role is not associated with this user"}), 304
