from flask import Blueprint, request

from app.services.permissions_service import *

permissions_bp = Blueprint('permissions_bp', __name__, url_prefix='/permissions')


@permissions_bp.route('', methods=['GET', 'POST'])
def permissions():
    if request.method == 'GET':
        return get_all_permissions()
    elif request.method == 'POST':
        data = request.json
        return get_all_permissions(data['page'])


@permissions_bp.route('/add_permission', methods=['POST'])
def create_permission():
    return add_one_permission()


@permissions_bp.route('/<string:permission_id>', methods=['GET', 'PUT', 'DELETE'])
def permission(permission_id):
    if request.method == 'GET':
        return get_one_permission(permission_id)
    elif request.method == 'PUT':
        return update_one_permission(permission_id)
    elif request.method == 'DELETE':
        return delete_one_permission(permission_id)


@permissions_bp.route('/permissions_by_group', methods=['GET'])
def permissions_by_group():
    return get_permissions_by_group()
