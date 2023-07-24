from bson import ObjectId
from flask import jsonify,  request, abort
from app.repositories.reviews_repository import ReviewsRepository
from app.models.reviews_model import Review
reviews_repo = ReviewsRepository()


def get_all_reviews(page=None):
    if page is not None:
        return reviews_repo.findAll(page, 15)
    else:
        return reviews_repo.findAll()


def get_one_review(review_id):
    review = reviews_repo.findById(review_id)
    if not review:
        abort(401)
    return review


def add_one_review():
    data = request.json
    if reviews_repo.query({
        'user_id': data['user_id'],
        'site_id': data['site_id']
    }):
        return jsonify({'error': 'User already submitted a review'}), 400

    review = Review(
        site_id=data['site_id'],
        user_id=data['user_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    review_data = reviews_repo.save(review)
    return jsonify(review_data)


def update_one_review(review_id):
    data = request.json
    review = get_one_review(review_id)
    if 'site_id' in data:
        review['site_id'] = data['site_id']
    if 'user_id' in data:
        review['user_id'] = data['user_id']
    if 'rating' in data:
        review['rating'] = data['rating']
    if 'comment' in data:
        review['comment'] = data['comment']

    return reviews_repo.update(review_id, review)


def delete_one_review(review_id):
    if reviews_repo.existsByField('_id', ObjectId(review_id)):
        return reviews_repo.delete(review_id)
    else:
        return abort(401)


def reviews_by_site(site_id):
    try:
        reviews = reviews_repo.findAllByField('site_id', site_id)
        return reviews
    except Exception as e:
        return jsonify({"error": str(e)}), 401


def reviews_by_user(user_id):
    try:
        return reviews_repo.findAllByField('user_id', user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 401


def average_rating_by_site(site_id):
    if reviews_repo.existsByField('site_id', site_id):
        return reviews_repo.averageRating(site_id)
    else:
        return jsonify({'error': 'Site not exists'}), 400
