from flask import Blueprint, jsonify, request, abort
import pymongo
from app.models import SiteStats, Site
from datetime import datetime
from app.repositories.site_stats_repository import SiteStatsRepository
from app.repositories.site_repository import SiteRepository
from app.services.site_stats_service import *

site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()

site_stats_bp = Blueprint('site_stats_bp', __name__, url_prefix='/site_stats')


@site_stats_bp.route('/top6_saved', methods=['GET'])
def search_sites():
    return search_top_six()


@site_stats_bp.route('/add_stats', methods=['POST'])
def create_stats():
    return add_stats()


@site_stats_bp.route('/<stat_id>', methods=['GET', 'PUT', 'DELETE'])
def site_stat(stat_id):
    if request.method == 'GET':
        return get_one_site_stats(stat_id)

    elif request.method == 'PUT':
        return update_one_site_stats(stat_id)

    elif request.method == 'DELETE':
        return delete_one_site_stats(stat_id)
