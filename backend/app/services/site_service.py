from flask import jsonify,  request, abort
import pymongo
from app.repositories.site_repository import SiteRepository
from app.repositories.user_site_repository import UserSiteRepository
from app.repositories.site_stats_repository import SiteStatsRepository
from app.services.user_site_service import query_referenced, query_not_referenced
from app.models.site_model import Site
from bson.objectid import ObjectId
from ..utils.s3Upload import uploadFile
from ..utils.faviconHelper import getFaviconFromURL
from app.utils.logger import logger
import json

site_repo = SiteRepository()
user_site_repo = UserSiteRepository()
site_stats_repo = SiteStatsRepository()


def get_all_sites(page=None):
    if page is not None:
        sites_data = site_repo.findAll(page, 15)
    else:
        sites_data = site_repo.findAll()
    return sites_data
    


def create_site():
    media_links = []
    data = json.loads(request.form['json'])

    if site_repo.existsByField('url', data['url']):
        return jsonify({"error": "Site already exists"}), 400

    if site_repo.existsByField('admin_email', data['admin_email']):
        return jsonify({"error": "This email is the admin for another site"}), 400

    if 'media' in request.files:
        data_media = request.files.getlist('media')
        if len(data_media) > 0:
            for file in data_media:
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
        return jsonify(site_data)
    except Exception as e:
        return jsonify({"error": "Error saving site",
                        "message": str(e)}), 400


def get_one_site(site_id):
    site = site_repo.findById(site_id)
    if not site:
        abort(401)
    return site


def update_one_site(site_id):
    media_links = []
    data = json.loads(request.form['json'])
    site = get_one_site(site_id)

    if 'media' in request.files:
        data_media = request.files.getlist('media')
        if len(data_media) > 0:
            for file in data_media:
                image_name = f"{data['name']}_{file.filename}"
                try:
                    file_data = file.stream.read()
                    file_link = uploadFile(file_data, image_name)
                    media_links.append(file_link)
                except Exception as e:
                    logger.error("Error uploading file " + str(e))
                    return jsonify({"error": "Error processing file",
                                    "message": str(e)}), 400

    if 'url' in data:
        site['url'] = data['url']
    if 'name' in data:
        site['name'] = data['name']
    if 'description' in data:
        site['description'] = data['description']
    if 'keywords' in data:
        site['keywords'] = data['keywords']
    if len(media_links) > 0:
        site['media'] = media_links
    if 'admin_email' in data:
        site['admin_email'] = data['admin_email']

    return site_repo.update(site_id, site)


def delete_one_site(site_id):
    get_one_site(site_id)
    if user_site_repo.existsByField('site._id', ObjectId(site_id)):
        user_site_repo.deleteAllSitesReferenceds(site_id)
    return site_repo.delete(site_id)


def search_sites_logged(user_id, page=None):
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    if page is not None:
        return site_repo.query(query_not_referenced(user_id, query), page, 15)
    else:
        return site_repo.query(query_not_referenced(user_id, query))



def search_sites_saves_logged(user_id, page=None):
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    if page is not None:
        return site_repo.query(query_referenced(user_id, query), page, 15)
    else:
        return site_repo.query(query_referenced(user_id, query))


def search_sites_not_logged():
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


def search_sites_name_suggested():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400

    pipeline = [
        {
            '$match': {
                '$or': [
                    {'url': {'$regex': query, '$options': 'i'}},
                    {'name': {'$regex': query, '$options': 'i'}}
                ]
            }
        },
        {
            '$sort': {'site_stats.saves': -1}
        },
        {
            '$limit': 10
        },
        {
            '$project': {'_id': 0, 'name': 1}
        }
    ]
    return site_repo.queryAggregation(pipeline)


def get_top_six_saved():
    top6_sites = site_repo.sort('site_stats.saves', pymongo.DESCENDING)[:6]
    return jsonify(top6_sites)


def stats_by_site(site_id):
    site = site_repo.findById(site_id)

    if not site:
        abort(404)

    if not site['site_stats']:
        abort(404)

    stats = site_stats_repo.findById(site['site_stats'])

    if not stats:
        abort(404)
    return stats
