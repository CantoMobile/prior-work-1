from flask import jsonify, request, abort
from models import Permissions
from repositories.permissions_repository import PermissionsRepository
from . import permissions_bp
permissions_repo = PermissionsRepository()


@permissions_bp.route('/permissions', methods=['GET', 'POST'])
def permissions():
    if request.method == 'GET':
        permissions_data = permissions_repo.findAll()
        return permissions_data
    elif request.method == 'POST':
        data = request.json
        permissions = Permissions(
            resource=data['resource'],
            actions=data['actions']
        )
        permissions_d = permissions_repo.save(permissions)
        return permissions_d


@permissions_bp.route('/permissions/<string:permission_id>', methods=['GET', 'PUT', 'DELETE'])
def permission(permission_id):
    permissions_data = permissions_repo.findById(permission_id)
    if not permissions_data:
        abort(404)

    if request.method == 'GET':
        return permissions_data

    elif request.method == 'PUT':
        data = request.json
        if 'resource' in data:
            permissions_data['resource'] = data['resource']
        if 'actions' in data:
            permissions_data['actions'] = data['actions']
        return permissions_repo.update(permission_id, permissions_data)

    elif request.method == 'DELETE':
        permissions_repo.delete(permission_id)
        return jsonify({"message": "Permission deleted"})


@permissions_bp.route('/permissions/permissions_by_group', methods=['GET'])
def permissions_by_group():
    query = request.args.get('query')
    if not query:
        abort(404)
    permissions = permissions_repo.query({
        '$or': [
            {'resource': {'$regex': query, '$options': 'i'}},
            {'actions': {'$regex': query, '$options': 'i'}}
        ]
    })
    return permissions
