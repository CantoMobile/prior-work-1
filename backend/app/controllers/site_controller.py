from flask import Blueprint, jsonify, request, abort
from app.models import Site
from app.repositories.site_repository import SiteRepository
from app.repositories.site_stats_repository import SiteStatsRepository
from app.services.user_site_service import return_not_referenced
from ..utils.s3Upload import uploadFile


site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()

site_bp = Blueprint('site_bp', __name__, url_prefix='/sites')
@site_bp.route('/', methods=['GET', 'POST'])
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
        site_data = site_repo.save(site)
        return jsonify(site_data)


@site_bp.route('/<site_id>', methods=['GET', 'PUT', 'DELETE'])
def site(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if request.method == 'GET':
        return site

    elif request.method == 'PUT':
        data = request.json

        if 'url' in data:
            site['url'] = data['url']
        if 'name' in data:
            site['name'] = data['name']
        if 'description' in data:
            site['description'] = data['description']
        if 'keywords' in data:
            site['keywords'] = data['keywords']
        if 'media' in data:
            site['media'] = data['media']
        if 'admin_email' in data:
            site['admin_email'] = data['admin_email']

        return site_repo.update(site_id, site)

    elif request.method == 'DELETE':
        site_repo.delete(site_id)
        return '', 204


@site_bp.route('/search', methods=['GET'])
def search_sites():
    query = request.args.get('query')
    # Get the search query from the request parameters
    if not query:
        return jsonify({'error': 'Missing search query'}), 400

    sites = site_repo.query({
        '$or': [
             {'url': {'$regex': query, '$options': 'i'}},
            {'name': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}},
            {'keywords': {'$regex': query, '$options': 'i'}}
        ]
    })
    return sites


@site_bp.route('/<site_id>/stats', methods=['GET'])
def site_stats(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if not site['site_stats']:
        abort(404)

    stats = site_stats_repo.findById(site['site_stats'])

    if not stats:
        abort(404)
    return stats

@site_bp.route('/user/<user_id>', methods=['GET'])
def get_sites_by_user(user_id):
    return return_not_referenced(user_id)
     