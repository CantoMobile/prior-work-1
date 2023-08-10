from flask import Blueprint
from app.services.user_site_service import *

user_sites_bp = Blueprint('user_sites_bp', __name__, url_prefix='/user_sites')


@user_sites_bp.route('/<relationship_id>', methods=['GET', 'DELETE'])
def user_site(relationship_id):
    if request.method == 'GET':
        return get_one_user_site(relationship_id)

    elif request.method == 'DELETE':
        return delete_one_user_site(relationship_id)


@user_sites_bp.route('', methods=['GET', 'POST'])
def user_sites():
    if request.method == 'GET':
        return get_all_user_sites()

    elif request.method == 'POST':
        data = request.json
        return get_all_user_sites(data['page'])


@user_sites_bp.route('/add_relationship', methods=['POST'])
def add_relationship():
    return add_user_site_relationship()


@user_sites_bp.route('/<user_id>/add_site/<site_id>', methods=['PUT'])
def add_site_user(user_id, site_id):
    return add_site(user_id, site_id)


@user_sites_bp.route('/<user_id>/remove_site/<site_id>', methods=['PUT'])
def remove_site_user(user_id, site_id):
    return remove_site(user_id, site_id)
