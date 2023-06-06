from flask import Blueprint, jsonify, request, abort
from app.models import Role, Permissions
from app.repositories.role_repository import RoleRepository
from app.repositories.permissions_repository import PermissionsRepository
from app.services.middleware import validate_token

permissions_repo = PermissionsRepository()
role_repo = RoleRepository()

role_bp = Blueprint('role_bp', __name__, url_prefix='/roles')
@role_bp.route('/', methods=['GET', 'POST'])
@validate_token
def roles():
    if request.method == 'GET':
        roles_data = role_repo.findAll()
        return roles_data

    elif request.method == 'POST':
        data = request.json
        if role_repo.existsByField('name', data['name'].title()):
            return {"error":"This role is already exist."}, 401
        role = Role(
            name=data['name'],
            description=data['description'],
            permissions=data['permissions']
        )
        role_data = role_repo.save(role)
        return jsonify(role_data)


@role_bp.route('/<role_id>', methods=['GET', 'PUT', 'DELETE'])
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


@role_bp.route('/<role_id>/add_permissions/<permission_id>', methods=['PUT'])
def add_role_permissions(role_id, permission_id):
    role_data = role_repo.findById(role_id)
    permission_data = permissions_repo.findById(permission_id)
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


@role_bp.route('/<role_id>/remove_permissions/<permission_id>', methods=['PUT'])
def remove_role_permissions(role_id, permission_id):
    role_data = role_repo.findById(role_id)
    permission_data = permissions_repo.findById(permission_id)
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
