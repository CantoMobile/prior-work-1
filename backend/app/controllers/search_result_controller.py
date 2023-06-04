from flask import Blueprint, jsonify, request, abort
from app.models import SearchResult, Site
from app.repositories.search_result_repository import SearchResultRepository
from app.repositories.site_repository import SiteRepository

site_repo = SiteRepository()
search_result_repo = SearchResultRepository()

search_results_bp = Blueprint('search_results_bp', __name__, url_prefix='/search_results')

@search_results_bp.route('/', methods=['GET', 'POST'])
def search_results():
    if request.method == 'GET':
        results_data = search_result_repo.findAll()
        return results_data

    elif request.method == 'POST':
        data = request.json
        site = site_repo.findById(data['site_id'])

        if not site:
            abort(404)

        search_result = SearchResult(
            query_string=data['query_string'],
            results=data['results'],
            site=data['site_id']
        )
        result_d = search_result_repo.save(search_result)
        result_data = result_d.__dict__.copy()
        result_data.pop('collection', None)
        result_data.pop('_id', None)
        result_data['site'] = str(result_data.get('site'))

        return jsonify(result_data)


@search_results_bp.route('/<result_id>', methods=['GET', 'PUT', 'DELETE'])
def search_result(result_id):
    result = search_result_repo.findById(result_id)

    if not result:
        abort(404)

    if request.method == 'GET':
        result_data = result.__dict__.copy()
        result_data.pop('collection', None)
        result_data.pop('_id', None)
        result_data['site'] = str(result_data.get('site'))

        return jsonify(result_data)

    elif request.method == 'PUT':
        data = request.json
        result.query_string = data['query_string']
        result.results = data['results']
        result = search_result_repo.update(result_id, result)
        result_data = result.__dict__.copy()
        result_data.pop('collection', None)
        result_data.pop('_id', None)
        result_data['site'] = str(result_data.get('site'))

        return jsonify(result_data)

    elif request.method == 'DELETE':
        search_result_repo.delete(result_id)
        return '', 204
