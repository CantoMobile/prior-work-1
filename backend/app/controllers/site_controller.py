from flask import jsonify, request, abort
from models import Site, SiteStats
from . import site_bp
from repositories.site_repository import SiteRepository
from repositories.site_stats_repository import SiteStatsRepository


site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()


@site_bp.route('/sites', methods=['GET', 'POST'])
def sites():
    if request.method == 'GET':
        sites_data = site_repo.findAll()
        return sites_data

    elif request.method == 'POST':
        data = request.json
        site = Site(
            url=data['url'],
            name=data['name'],
            description=data['description'],
            keywords=data['keywords'],
            media=data['media'],
            admin_email=data['admin_email']
        )
        site_d = site_repo.save(site)
        site_data = site_d.__dict__.copy()
        site_data.pop('collection', None)
        site_data.pop('_id', None)
        site_data['site_stats'] = str(site_data.get('site_stats'))
        return jsonify(site_data)


@site_bp.route('/sites/<site_id>', methods=['GET', 'PUT', 'DELETE'])
def site(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if request.method == 'GET':
        site_data = site.__dict__.copy()
        site_data.pop('collection', None)
        site_data.pop('_id', None)
        site_data['site_stats'] = str(site_data.get('site_stats'))

        return jsonify(site_data)

    elif request.method == 'PUT':
        data = request.json
        site.url = data['url']
        site.name = data['name']
        site.description = data['description']
        site.keywords = data['keywords']
        site.media = data['media']
        site.admin_email = data['admin_email']
        site = site_repo.update(site_id, site)
        site_data = site.__dict__.copy()
        site_data.pop('collection', None)
        site_data.pop('_id', None)
        site_data['site_stats'] = str(site_data.get('site_stats'))

        return jsonify(site_data)

    elif request.method == 'DELETE':
        site_repo.delete(site_id)
        return '', 204


@site_bp.route('/sites/<site_id>/stats', methods=['GET'])
def site_stats(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if not site.site_stats:
        abort(404)

    stats = site_stats_repo.findById(site.site_stats)

    if not stats:
        abort(404)

    stats_data = {
        'visits': stats.visits,
        'unique_visitors': stats.unique_visitors,
        'last_visit': stats.last_visit.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(stats_data)
