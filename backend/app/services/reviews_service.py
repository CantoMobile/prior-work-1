from flask import jsonify,  request, abort

from app.repositories.reviews_repository import ReviewsRepository
reviews_repo = ReviewsRepository()


def reviews_by_site(site_id):
    try:
        reviews = reviews_repo.findAllByField('site_id', site_id)
        return jsonify(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
def reviews_by_user(user_id): 
    reviews = reviews_repo.findAllByField('user_id', user_id)
    return jsonify({reviews})
