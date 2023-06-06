from flask import Blueprint, jsonify, request, abort
from app.models import Permissions
from app.repositories.permissions_repository import PermissionsRepository
permissions_repo = PermissionsRepository()


permissions_bp = Blueprint('permissions_bp', __name__, url_prefix='/permissions')

@permissions_bp.route('/', methods=['GET', 'POST'])
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


@permissions_bp.route('/<string:permission_id>', methods=['GET', 'PUT', 'DELETE'])
def permission(permission_id):
    permissions_data = permissions_repo.findById(permission_id)
    if not permissions_data:
        abort(404)

    if request.method == 'GET':
        return permissions_data

    elif request.method == 'PUT':
        data = request.json
        updated_permissions = permissions_data.copy()
        if 'resource' in data:
            updated_permissions['resource'] = data['resource']
        if 'actions' in data:
            updated_permissions['actions'] = data['actions']
        return permissions_repo.update(permission_id, updated_permissions)

    elif request.method == 'DELETE':
        update = ["role","permissions"]
        try:
            permissions_repo.deleteFromArrayMany(permission_id, update, update[0])
            permissions_repo.delete(permission_id)
            return jsonify({"message": "Permission deleted"})
        except Exception as e:
            return jsonify({"message": "Failed to delete permission", "error": str(e)}), 401



@permissions_bp.route('/permissions_by_group', methods=['GET'])
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
