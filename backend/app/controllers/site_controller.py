from flask import Blueprint, jsonify, request, abort
import json

import pymongo
from app.models import Site
from app.repositories.site_repository import SiteRepository
from app.repositories.site_stats_repository import SiteStatsRepository
from app.repositories.reviews_repository import ReviewsRepository
from app.repositories.user_repository import UserRepository
from app.services.user_site_service import query_referenced, return_not_referenced, return_referenced, query_not_referenced
from ..utils.s3Upload import uploadFile
from ..utils.faviconHelper import getFaviconFromURL
from app.utils.logger import logger

site_stats_repo = SiteStatsRepository()
site_repo = SiteRepository()
reviews_repo = ReviewsRepository()
user_repo = UserRepository()

site_bp = Blueprint('site_bp', __name__, url_prefix='/sites')


@site_bp.route('/', methods=['GET'])
def sites():
    sites_data = site_repo.findAll()
    return sites_data


@site_bp.route('/add_site', methods=['POST'])
def add_site():
    media_links = []
    data = json.loads(request.form['json'])

    if site_repo.existsByField('url', data['url']):
        return jsonify({"error": "Site already exists"}), 400

    if 'media' in request.files and (request.files['media']):
        for file in request.files.getlist('media'):
            image_name = f"{data['name']}_{file.filename}"
            try:
                file_data = file.stream.read()
                file_link = uploadFile(file_data, image_name)
                media_links.append(file_link)
            except Exception as e:
                logger.error("Error uploading file " + str(e))
                return jsonify({"error": "Error processing file",
                                "message": str(e)}), 400
    site = Site(
        url=data['url'],
        name=data['name'],
        description=data['description'],
        logo=getFaviconFromURL(data['url']),
        keywords=data['keywords'],
        media=media_links,
        admin_email=data['admin_email'] if 'admin_email' in data else ""
    )
    try:
        site_data = site_repo.save(site)
        print(site_data)
        return jsonify(site_data)
    except Exception as e:
        return jsonify({"error": "Error saving site",
                        "message": str(e)}), 400


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


@site_bp.route('/<site_id>/reviews', methods=['GET'])
def site_reviews(site_id):
    try:
        reviews = reviews_repo.findAllByField('site_id', site_id)
        
        return jsonify(reviews)

    except Exception as e:

        return jsonify({'error': str(e)}), 500

@site_bp.route('/<user_id>/search', methods=['GET'])
def search_sites(user_id):
    query = request.args.get('query')
    # Get the search query from the request parameters
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    return site_repo.query(query_not_referenced(user_id, query))

@site_bp.route('/<user_id>/search_saves', methods=['GET'])
def search_sites_saves(user_id):
    query = request.args.get('query')
    # Get the search query from the request parameters
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    return site_repo.query(query_referenced(user_id, query))


@site_bp.route('/search', methods=['GET'])
def search_sites_logout():
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


@site_bp.route('/not_user/<user_id>', methods=['GET'])
def get_sites_not_ref_by_user(user_id):
    return return_not_referenced(user_id)


@site_bp.route('/user/<user_id>', methods=['GET'])
def get_sites__ref_by_user(user_id):
    return return_referenced(user_id)

@site_bp.route('/top6_saved', methods=['GET'])
def search_top_six_sites():
    top6_sites = site_repo.sort('site_stats.saves', pymongo.DESCENDING)[:6]
    return jsonify(top6_sites)
