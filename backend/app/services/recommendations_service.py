from bson import ObjectId
from flask import abort, jsonify, request
from app.repositories.recommendations_repository import RecommendationsRepository
from app.models.recommendations_model import Recommendation
from app.repositories.user_repository import UserRepository
from app.repositories.site_repository import SiteRepository
from app.utils.RecommendationSystem import HybridModel
from app.utils.logger import logger
import json


recommendations_repo = RecommendationsRepository()
user_repo = UserRepository()
site_repo = SiteRepository()


def get_one_user_recommendations(user_id):
    recommendations = recommendations_repo.findByField('user_id', user_id)
    if not recommendations:
        abort(401)
    return recommendations

def add_one_user_recommendations(user_id):
    if recommendations_repo.findByField('user_id', user_id):
        abort(404)

    recommendation_model = HybridModel(user_repo.findAll(), site_repo.findAll())
    user = user_repo.findById(user_id)
    if not user:
        abort(401)
    
    user_name = user['name']
    recommendations = recommendation_model.get_user_hybrid_recommendations(user_id, user_name)
    if recommendations == {"message": "User has no saved sites."}:
        return jsonify({"message": "User has no saved sites."})
    
    user_recommendations = Recommendation(
        user_id,
        recommendations
    )

    try:
        recommendations_data = recommendations_repo.save(user_recommendations)
        return jsonify(recommendations_data)
    except Exception as e:
        return jsonify({"error": "Error saving recommendations",
        "message": str(e)}), 400


def update_one_user_recommendations(user_id):
    user_recommendations = get_one_user_recommendations(user_id)

    # new_user_recommendations = get_recommendations(user_id)
    # user_recommendations['recommendations'] = new_user_recommendations
 

    return recommendations_repo.update(user_id, user_recommendations)