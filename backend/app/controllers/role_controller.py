from flask import Blueprint, request

from app.services.middleware import validate_token
from app.services.role_service import *

role_bp = Blueprint('role_bp', __name__, url_prefix='/roles')


@role_bp.route('', methods=['GET', 'POST'])
@validate_token
def roles():
    if request.method == 'GET':
        return get_all_roles()

    elif request.method == 'POST':
        data = request.json
        return get_all_roles(data['page'])


@role_bp.route('/add_role', methods=['POST'])
def add_role():
    return create_role()


@role_bp.route('/<role_id>', methods=['GET', 'PUT', 'DELETE'])
def role(role_id):
    if request.method == 'GET':
        return get_one_role

    elif request.method == 'PUT':
        return update_one_role(role_id)

    elif request.method == 'DELETE':
        return delete_one_role(role_id)


@role_bp.route('/<role_id>/add_permissions/<permission_id>', methods=['PUT'])
def add_role_permissions(role_id, permission_id):
    return add_permissions(role_id, permission_id)


@role_bp.route('/<role_id>/remove_permissions/<permission_id>', methods=['PUT'])
def remove_role_permissions(role_id, permission_id):
    return remove_permissions(role_id, permission_id)
