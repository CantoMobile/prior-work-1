from flask import Blueprint, jsonify, request, abort
import json
from app.models import Site
from app.repositories.site_repository import SiteRepository
from app.repositories.site_stats_repository import SiteStatsRepository
from ..utils.s3Upload import uploadFile


site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()

site_bp = Blueprint('site_bp', __name__, url_prefix='/sites')
@site_bp.route('/', methods=['GET', 'POST'])
def sites():
    sites_data = site_repo.findAll()
    return sites_data


@site_bp.route('/add_site', methods=['POST'])
def add_site():
        media_links = []
        data = json.loads(request.form['json'])
        
        if (request.files != None):
            for file in request.files.getlist('media'):
                image_name = f"{data['name']}_{file.filename}"
                try:
                    file_data = file.stream.read()
                    file_link = uploadFile(file_data, image_name)
                except Exception as e:
                    return e
                media_links.append(file_link)

        site = Site(
            url=data['url'],
            name=data['name'],
            description=data['description'],
            keywords=data['keywords'],
            media=media_links,
            admin_email=data['admin_email'] if 'admin_email' in data else ""
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
