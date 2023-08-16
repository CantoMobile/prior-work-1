from flask import Blueprint, jsonify, request, abort
from app.repositories.recommendations_repository import RecommendationsRepository
from app.services.recommendations_service import *
recommendations_repo = RecommendationsRepository()


recommendations_bp = Blueprint('recommendations_bp', __name__, url_prefix='/recommendations')

@recommendations_bp.route('/', methods=['GET'])
def all_recommendations():
    logger.info("here")
    return jsonify({'hey': 'hi'})



@recommendations_bp.route('/<user_id>/recommendations', methods=['GET', 'POST', 'PUT'])
def recommendations(user_id):
    if request.method == 'GET':
        return get_one_user_recommendations(user_id)
    elif request.method == 'POST':
        return add_one_user_recommendations(user_id)
    elif request.method == 'PUT':
        return update_one_user_recommendations(user_id)