from flask import jsonify, request, abort
from models import Role
from models import Permissions
from . import role_bp
from repositories.role_repository import RoleRepository
from repositories.permissions_repository import PermissionsRepository

permissions_repo = PermissionsRepository()
role_repo = RoleRepository()


@role_bp.route('/roles', methods=['GET', 'POST'])
def roles():
    if request.method == 'GET':
        roles_data = role_repo.findAll()
        return roles_data

    elif request.method == 'POST':
        data = request.json
        role = Role(
            name=data['name'],
            description=data['description'],
            permissions=data['permissions']
        )
        role_data = role_repo.save(role)
        return jsonify(role_data)


@role_bp.route('/roles/<role_id>', methods=['GET', 'PUT', 'DELETE'])
def role(role_id):
    role = role_repo.findById(role_id)
    if not role:
        abort(404)

    if request.method == 'GET':
        return role

    elif request.method == 'PUT':
        data = request.json
        if 'name' in data:
            role['name'] = data['name']
        if 'description' in data:
            role['description'] = data['description']
        if 'permissions' in data:
            role['permissions'] = data['permissions']
        return role_repo.update(role_id, role)

    elif request.method == 'DELETE':
        role_repo.delete(role_id)
        return '', 204


@role_bp.route('/roles/<role_id>/add_permissions/<permission_id>', methods=['PUT'])
def add_role_permissions(role_id, permission_id):
    role_data = role_repo.findById(role_id)
    print(role_data)
    permission_data = permissions_repo.findById(permission_id)
    print(permission_data)
    if not role_data or not permission_data:
        abort(404)
    role = Role(**role_data)
    permission = Permissions(**permission_data)
    validation = any(
        permission_item['_id'] == permission_id for permission_item in role.permissions)
    if validation:
        return {'Error': 'The role is already assigned this permission'}, 404
    else:
        return role_repo.updateArray(role_id, 'permissions', permission)


@role_bp.route('/roles/<role_id>/remove_permissions/<permission_id>', methods=['PUT'])
def remove_role_permissions(role_id, permission_id):
    role_data = role_repo.findById(role_id)
    print(role_data)
    permission_data = permissions_repo.findById(permission_id)
    print(permission_data)
    if not role_data or not permission_data:
        abort(404)
    role = Role(**role_data)
    permission = Permissions(**permission_data)
    validation = any(
        permission_item['_id'] == permission_id for permission_item in role.permissions)
    if validation:
        return role_repo.deleteFromArray(role_id, 'permissions', permission)
    else:
        return {"Error": "This permission is not associated with this role"}, 404
