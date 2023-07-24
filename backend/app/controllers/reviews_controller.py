from flask import Blueprint, request

from app.services.reviews_service import *

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix='/reviews')


@reviews_bp.route('', methods=['GET', 'POST'])
def sites():
    if request.method == 'GET':
        return get_all_reviews()
    elif request.method == 'POST':
        data = request.json
        return get_all_reviews(data['page'])


@reviews_bp.route('/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    if request.method == 'GET':
        return get_one_review(review_id)

    elif request.method == 'PUT':
        return update_one_review(review_id)

    elif request.method == 'DELETE':
        return delete_one_review(review_id)


@reviews_bp.route('/<site_id>/average_rating', methods=['GET'])
def site_average_rating_reviews(site_id):
    return average_rating_by_site(site_id)


@reviews_bp.route('/add_review', methods=['POST'])
def add_review():
    return add_one_review()


@reviews_bp.route('/user/<user_id>', methods=['GET'])
def get_reviews_by_user(user_id):
    return reviews_by_user(user_id)


@reviews_bp.route('/site/<site_id>', methods=['GET'])
def get_reviews_by_site(site_id):
    return reviews_by_site(site_id)
