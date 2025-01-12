from flask import Blueprint, Response
from flask_cors import cross_origin
from app.services.user_site_service import return_not_referenced, return_referenced
from app.services.middleware import admin_permission_required
from app.services.site_service import *
from app.services.user_service import add_created_site_user, get_created_sites_user
from app.utils.UploadMasiveSites import upload_masive_sites
from app.config.database import Database
import numpy as np


site_bp = Blueprint('site_bp', __name__, url_prefix='/sites')


@site_bp.route('', methods=['GET', 'POST'])
def sites():
    if request.method == 'POST':
        data = request.json
        return get_all_sites(data['page'])
    elif request.method == 'GET':
        return get_all_sites()

#IMPORTANT
@site_bp.route('/add_site', methods=['POST'])
def add_site():
    return create_site()

#IMPORTANT
@site_bp.route('/<site_id>', methods=['POST','GET', 'PUT', 'DELETE'])
# @admin_permission_required
def site(site_id):
    if request.method == 'GET':
        return get_one_site(site_id)
    elif request.method == 'POST':
        return get_one_site_discrimined(site_id)

    elif request.method == 'PUT':
        return update_one_site(site_id)

    elif request.method == 'DELETE':
        return delete_one_site(site_id)


@site_bp.route('/<user_id>/search', methods=['GET'])
def search_sites(user_id):
    # if request.method == 'GET':
    #     return search_sites_logged(user_id)
    # elif request.method == 'POST':
    #     data = request.json
    #     return search_sites_logged(user_id, data['page'])
    if request.method == 'GET':
        return search_all_sites_discrimied(user_id)


@site_bp.route('/search_admin', methods=['POST'])
def search_admin():
    data = request.json
    return search_sites_claimed(data['page'])


@site_bp.route('/<user_id>/search_saves', methods=['GET', 'POST'])
def search_sites_saves(user_id):
    if request.method == 'GET':
        return search_sites_saves_logged(user_id)
    elif request.method == 'POST':
        data = request.json
        return search_sites_saves_logged(user_id, data['page'])


@site_bp.route('/<user_id>/created', methods=['GET', 'POST'])
def search_created_sites(user_id):
    if request.method == 'GET':
        return get_created_sites_user(user_id)
    elif request.method == 'POST':
        data = request.json
        return get_created_sites_user(user_id, data['page'])
    
@site_bp.route('/get_lastest_added', methods=['GET'])
def get_lastest_added():
    return get_lastest_added_sites()


@site_bp.route('/search', methods=['GET'])
def search_sites_logout():
    return search_sites_not_logged()


@site_bp.route('/search_suggested', methods=['GET'])
def search_sites_suggested():
    return search_sites_name_suggested()


@site_bp.route('/<site_id>/stats', methods=['GET'])
def site_stats(site_id):
    return stats_by_site(site_id)


@site_bp.route('/not_user/<user_id>', methods=['GET', 'POST'])
def get_sites_not_ref_by_user(user_id):
    if request.method == 'GET':
        return return_not_referenced(user_id)
    if request.method == 'POST':
        data = request.json
        return return_not_referenced(user_id, data['page'])


@site_bp.route('/user/<user_id>', methods=['GET', 'POST'])
def get_sites__ref_by_user(user_id):
    if request.method == 'GET':
        return return_referenced(user_id)
    elif request.method == 'POST':
        data = request.json
        return return_referenced(user_id, data['page'])


@site_bp.route('/top6_saved', methods=['GET'])
def search_top_six_sites():
    return get_top_six_saved()


@site_bp.route('/top6_saved_logged/<user_id>', methods=['GET'])
def search_top_six_saved_logged(user_id):
    return get_top_six_saved_logged(user_id)

@site_bp.route('/user_id/<user_id>', methods=['GET'])
def search_discrimined_sites(user_id):
    return get_all_sites_discrimined(user_id)


@site_bp.route('/<user_id>/save_site/<site_id>', methods=['PUT'])
def save_site(user_id, site_id):
    return add_created_site_user(site_id, user_id)

#IMPORTANT
@site_bp.route('/update_icon/<site_id>', methods=['PUT'])
def update_icon_site(site_id):
    return update_site_icon(site_id)


@site_bp.route('/initialize', methods=['POST'])
def initialize_app():
    data = request.json
    return upload_masive_sites(data['path'])


@site_bp.route('/validate_otp', methods=['POST'])
@cross_origin()
def validate_otp():
    return validate_site_otp()


@site_bp.route('/create_otp', methods=['POST'])
def create_otp():
    return add_one_otp()


@site_bp.route('/<site_id>/delete_ownership', methods=['DELETE'])
def delete_ownership(site_id):
    return delete_site_ownership(site_id)
