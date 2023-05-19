from flask import jsonify, request, abort
from models import UserSite, User, Site
from . import user_sites_bp
from repositories.user_site_repository import UserSiteRepository
from repositories.user_repository import UserRepository
from repositories.site_repository import SiteRepository
user_repo = UserRepository()
user_site_repo = UserSiteRepository()
site_repo = SiteRepository()


@user_sites_bp.route('/user_sites', methods=['GET', 'POST'])
def user_sites():
    if request.method == 'GET':
        user_sites_data = user_site_repo.findAll()
        return user_sites_data

    elif request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        site_id = data.get('site_id')

        user = user_repo.findById(user_id)
        site = site_repo.findById(site_id)

        if not user or not site:
            abort(404)

        if UserSite.objects(user=user, site=site):
            return "User-site relationship already exists."

        user_site = UserSite(user=user, site=site)
        user_data = user_site_repo.save(user_site)

        response_data = {
            'user_id': str(user_data.user),
            'site_id': str(user_data.site)
        }

        return jsonify(response_data)


@user_sites_bp.route('/user_sites/<relationship_id>', methods=['GET', 'DELETE'])
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
