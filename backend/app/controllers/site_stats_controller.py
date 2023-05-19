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
        site_id = data.get('site_id')
        visits = data.get('visits', 0)
        unique_visitors = data.get('unique_visitors', 0)
        last_visit = datetime.strptime(data.get(
            'last_visit'), '%Y-%m-%d %H:%M:%S') if data.get('last_visit') else None

        site = site_repo.findById(site_id)

        if not site:
            abort(404)

        site_stats = SiteStats(
            site=site, visits=visits, unique_visitors=unique_visitors, last_visit=last_visit)
        site_stats = site_stats_repo.save(site_stats)
        response_data = {
            'site_id': str(site_stats.site),
            'visits': site_stats.visits,
            'unique_visitors': site_stats.unique_visitors,
            'last_visit': site_stats.last_visit.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(response_data)


@site_stats_bp.route('/site_stats/<stat_id>', methods=['GET', 'PUT', 'DELETE'])
def site_stat(stat_id):
    site_stats = site_stats_repo.findById(stat_id)

    if not site_stats:
        abort(404)

    if request.method == 'GET':
        stat_data = {
            'site_id': str(site_stats.site),
            'visits': site_stats.visits,
            'unique_visitors': site_stats.unique_visitors,
            'last_visit': site_stats.last_visit.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(stat_data)

    elif request.method == 'PUT':
        data = request.json
        site_stats.visits = data.get('visits', site_stats.visits)
        site_stats.unique_visitors = data.get(
            'unique_visitors', site_stats.unique_visitors)
        site_stats.last_visit = datetime.strptime(data.get(
            'last_visit'), '%Y-%m-%d %H:%M:%S') if data.get('last_visit') else None
        site_stats = site_stats_repo.update(stat_data, site_stats)

        response_data = {
            'site_id': str(site_stats.site),
            'visits': site_stats.visits,
            'unique_visitors': site_stats.unique_visitors,
            'last_visit': site_stats.last_visit.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify(response_data)

    elif request.method == 'DELETE':
        site_stats_repo.delete(stat_id)
        return '', 204
