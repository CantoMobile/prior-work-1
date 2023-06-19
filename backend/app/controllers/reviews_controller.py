from flask import Blueprint, jsonify, request, abort
import json
from app.models import Review
from app.repositories.reviews_repository import ReviewsRepository

reviews_repo = ReviewsRepository()

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix='/reviews')
@reviews_bp.route('/', methods=['GET'])
def sites():
    sites_data = reviews_repo.findAll()
    return sites_data


@reviews_bp.route('/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    review = reviews_repo.findById(review_id)

    if not review:
        abort(404)

    if request.method == 'GET':
        return review

    elif request.method == 'PUT':
        data = request.json
        if 'site_id' in data:
            review['site_id'] = data['site_id']
        if 'user_id' in data:
            review['user_id'] = data['user_id']
        if 'rating' in data:
            review['rating'] = data['rating']
        if 'comment' in data:
            review['comment'] = data['comment']

        return reviews_repo.update(review_id, review)

    elif request.method == 'DELETE':
        reviews_repo.delete(review_id)
        return '', 204


@reviews_bp.route('/add_review', methods=['POST'])
def add_review():
        data = json.loads(request.form['json']) 

        review = Review(
            site_id=data['site_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment']
        )

        review_data = reviews_repo.save(review)
        return jsonify(review_data)


@reviews_bp.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_reviews_by_user(user_id):
    try:
        reviews = reviews_repo.findAllByField('user_id', user_id)

        return jsonify(reviews)
    
    except Exception as e:

        return jsonify({'error': str(e)}), 500
