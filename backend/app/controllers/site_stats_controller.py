from flask import jsonify, request, abort
from models import SiteStats, Site
from datetime import datetime
from . import site_stats_bp
from repositories.site_stats_repository import SiteStatsRepository
from repositories.site_repository import SiteRepository

site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()


@site_stats_bp.route('/site_stats', methods=['GET', 'POST'])
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


@site_stats_bp.route('/site_stats/<stat_id>', methods=['GET', 'PUT', 'DELETE'])
def site_stat(stat_id):
    site_stats = site_stats_repo.findById(stat_id)
    print(site_stats)
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
