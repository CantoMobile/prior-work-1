from flask import Blueprint, request
from app.services.admin_service import *
from app.services.site_service import get_all_sites, delete_one_site, update_one_site

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/get_all_metrics', methods=['GET'])
def get_all_metrics():
    return get_admin_information()

@admin_bp.route('/get_all_sites', methods=['POST'])
def get_all_sites_admin():
    data = request.json
    return get_all_sites(data['page'])

@admin_bp.route('/<site_id>/delete', methods=['DELETE'])
def delete_site_admin(site_id):
    return delete_one_site(site_id)
