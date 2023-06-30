from bson import ObjectId
from flask import abort, jsonify, request
from app.models import Permissions, Role
from app.repositories.role_repository import RoleRepository
from app.repositories.permissions_repository import PermissionsRepository

role_repo = RoleRepository()
permissions_repo = PermissionsRepository()


def get_all_roles(page=None):
    if page is None:
        role_repo.findAll()
    else:
        role_repo.findAll(page, 15)


def create_role():
    data = request.json
    if role_repo.existsByField('name', data['name'].title()):
        return {"error": "This role is already exist."}, 401
    role = Role(
        name=data['name'],
        description=data['description']
    )
    role_data = role_repo.save(role)
    return role_data


def get_one_role(role_id):
    role = role_repo.findById(role_id)
    if not role:
        abort(401)
    return role


def update_one_role(role_id):
    role = get_one_role(role_id)
    data = request.json
    if 'name' in data:
        role['name'] = data['name']
    if 'description' in data:
        role['description'] = data['description']
    if 'permissions' in data:
        add_permissions(role_id, data['permissions'])
    return role_repo.update(role_id, role)


def delete_one_role(role_id):
    if role_repo.existsByField('_id', ObjectId(role_id)):
        return role_repo.delete(role_id)
    else:
        return jsonify({'Error': 'The role not exists'}), 304


def add_permissions(role_id, permission_id):
    role_data = get_one_role(role_id)
    permission_data = permissions_repo.findById(permission_id)
    role = Role(**role_data)
    permission = Permissions(**permission_data)
    validation = any(
        permission_item['_id'] == permission_id for permission_item in role.permissions)
    if validation:
        return {'Error': 'The role is already assigned this permission'}, 404
    else:
        return role_repo.updateArray(role_id, 'permissions', permission)


def remove_permissions(role_id, permission_id):
    role_data = get_one_role(role_id)
    permission_data = permissions_repo.findById(permission_id)
    role = Role(**role_data)
    permission = Permissions(**permission_data)
    validation = any(
        permission_item['_id'] == permission_id for permission_item in role.permissions)
    if validation:
        return role_repo.deleteFromArray(role_id, 'permissions', permission)
    else:
        return {"Error": "This permission is not associated with this role"}, 404


def extract_permissions(id_role):
    role = role_repo.findById(id_role)
    if len(role["permissions"]) == 0:
        return None
    else:
        extracted_permissions = set(
            (permission["resource"], permission["actions"]) for permission in role["permissions"])
        return extracted_permissions
