from flask import current_app, request, jsonify, abort
from models.role_model import Role
from models.user_model import User
from . import user_bp
from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
role_repo = RoleRepository()
user_repo = UserRepository()


@user_bp.route('/users', methods=['GET', 'POST'])
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
            password=data['password'],
            roles=roles
        )
        user_data = user_repo.save(user)
        return jsonify(user_data)


@user_bp.route('/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
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
        if 'password' in data:
            user_data['password'] = data['password']
        if 'roles' in data:
            user_data['roles'] = data['roles']
        return user_repo.update(user_id, user_data)

    elif request.method == 'DELETE':
        user_repo.delete(user_id)
        return jsonify({'message': 'User deleted'})


@user_bp.route('/users/<user_id>/verify_password', methods=['POST'])
def verify_user_password(user_id):
    data = request.json
    user_data = user_repo.findById(user_id)
    user_data.pop('_id')
    if not user_data:
        abort(404)

    user = User(**user_data)

    if user.verify_password(data['password']):
        return jsonify({'message': 'Password is correct'})
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
    response = user.set_password(data['password'])
    if response != None and response == True:
        update = user_repo.update(user_id, user)
        print("update:", update)
        return jsonify(update)
    else:
        return {"error": "Error al actualizar la contraseña"}, 304


@user_bp.route('/users/<user_id>/add_role/<role_id>', methods=['PUT'])
def add_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    user_data.pop('_id')
    role_data = role_repo.findById(role_id)
    role_data.pop('_id')
    if not user_data or not role_data:
        abort(404)

    user = User(**user_data)
    role = Role(**role_data)
    if role in user.roles:
        return {'Error': 'El usuario ya tiene el rol asignado'}, 304
    else:
        final_role = role_repo.findById(role_id)
        return user_repo.update_role(user_id, final_role)


@user_bp.route('/users/<user_id>/remove_role/<role_id>', methods=['PUT'])
def remove_user_role(user_id, role_id):
    user_data = user_repo.findById(user_id)
    user_data.pop('_id')
    role_data = role_repo.findById(role_id)
    role_data.pop('_id')

    if not user_data or not role_data:
        abort(404)

    user = User(**user_data)
    role = Role(**role_data)
    user.remove_role(role)
    return user_repo.update(user_id, user)
