from flask import abort, jsonify, request
from app.models import Permissions
from app.repositories.permissions_repository import PermissionsRepository
permissions_repo = PermissionsRepository()


def get_all_permissions(page=None):
    if page is not None:
        return permissions_repo.findAll(page, 15)
    else:
        return permissions_repo.findAll()


def get_one_permission(permission_id):
    permission = permissions_repo.findById(permission_id)
    if not permission:
        abort(401)
    return permission


def add_one_permission():
    data = request.json
    permissions = Permissions(
        resource=data['resource'],
        actions=data['actions']
    )
    permissions_d = permissions_repo.save(permissions)
    return permissions_d


def update_one_permission(permission_id):
    data = request.json
    updated_permissions = get_one_permission(permission_id)
    if 'resource' in data:
        updated_permissions['resource'] = data['resource']
    if 'actions' in data:
        updated_permissions['actions'] = data['actions']
    return permissions_repo.update(permission_id, updated_permissions)


def delete_one_permission(permission_id):
    update = ["role", "permissions"]
    try:
        permissions_repo.deleteFromArrayMany(
            permission_id, update, update[0])
        permissions_repo.delete(permission_id)
        return jsonify({"message": "Permission deleted"})
    except Exception as e:
        return jsonify({"message": "Failed to delete permission", "error": str(e)}), 401


def get_permissions_by_group():
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