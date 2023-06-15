from flask import Blueprint, jsonify, request, abort
from app.models import UserSite
from app.repositories.user_site_repository import UserSiteRepository
from app.repositories.user_repository import UserRepository
from app.repositories.site_repository import SiteRepository
from app.services.user_site_service import add_site, remove_site


user_repo = UserRepository()
user_site_repo = UserSiteRepository()
site_repo = SiteRepository()

user_sites_bp = Blueprint('user_sites_bp', __name__, url_prefix='/user_sites')


@user_sites_bp.route('/<relationship_id>', methods=['GET', 'DELETE'])
def user_site(relationship_id):
    user_site = user_site_repo.findById(relationship_id)

    if not user_site:
        abort(404)

    if request.method == 'GET':
        site_data = {
            'user_id': str(user_site.user),
            'site_id': str(user_site.site)
        }
        return jsonify(site_data)

    elif request.method == 'DELETE':
        user_site_repo.delete(relationship_id)
        return '', 204

@user_sites_bp.route('', methods=['GET', 'POST'])
def user_sites():
    if request.method == 'GET':
        user_site_data = user_site_repo.findAll()
        return user_site_data

    elif request.method == 'POST':
        data = request.json
        id_user = data['user_id']
        user = user_repo.findById(id_user)
        if not user:
            print("im here")
            abort(404)
        exists = user_site_repo.findByField('user_id', user['_id'])
        if exists != None:
            print("im here 2")
            abort(404)
        user_site = UserSite(user_id=user['_id'])
        user_site_data = user_site_repo.save(user_site)
        return user_site_data
    
@user_sites_bp.route('/<user_id>/add_site/<site_id>', methods=['PUT'])
def add_site_user(user_id,site_id):
    return add_site(user_id, site_id)

@user_sites_bp.route('/<user_id>/remove_site/<site_id>', methods=['PUT'])
def remove_site_user(user_id,site_id):
    return remove_site(user_id, site_id)



