from flask import Blueprint, jsonify, request, abort
import pymongo
from app.models import SiteStats, Site
from datetime import datetime
from app.repositories.site_stats_repository import SiteStatsRepository
from app.repositories.site_repository import SiteRepository

site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()

site_stats_bp = Blueprint('site_stats_bp', __name__, url_prefix='/site_stats')

@site_stats_bp.route('/', methods=['GET', 'POST'])
def site_stats():
    if request.method == 'GET':
        site_stats_data = site_stats_repo.findAll()
        return site_stats_data

    elif request.method == 'POST':
        data = request.json
        if 'site' in data:
            site = site_repo.findByField('url', data['site'])
            if not site:
                abort(404)
        site_stats = SiteStats(
            site={'_id': site['_id']}
        )
        site_stats_d = site_stats_repo.save(site_stats)
        site['site_stats'] = {'collection': 'sitestats',
                              '_id': site_stats_d['_id']
                              }
        site_repo.update(site['_id'], site)
        return site_stats_d

@site_stats_bp.route('/top6_saved', methods=['GET'])
def search_sites():
    top6_sites = site_stats_repo.sort('saves', pymongo.DESCENDING)[:6]
    return jsonify(top6_sites)

@site_stats_bp.route('/<stat_id>', methods=['GET', 'PUT', 'DELETE'])
def site_stat(stat_id):
    site_stats = site_stats_repo.findById(stat_id)
    if not site_stats:
        abort(404)

    if request.method == 'GET':
        return site_stats

    elif request.method == 'PUT':
        data = request.json
        if 'site' in data:
            site = site_repo.findByField('url', data['site'])
            if not site:
                abort(404)
            if site_stats['site']['_id'] != site['_id']:
                abort(404)

        if 'visits' in data:
            site_stats['visits'] += data['visits']
        if 'unique_visitors' in data:
            site_stats['unique_visitors'] += data['unique_visitors']
        site_stats['last_visit'] = datetime.now()

        return site_stats_repo.update(stat_id, site_stats)

    elif request.method == 'DELETE':
        site = site_repo.findByField('site_stats._id', stat_id)
        site['site_stats'] = None
        site_repo.update(site['_id'], site)
        site_stats_repo.delete(stat_id)
        return '', 204
