from flask import jsonify, request, abort
from models import Role
from . import role_bp
from repositories.role_repository import RoleRepository
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
