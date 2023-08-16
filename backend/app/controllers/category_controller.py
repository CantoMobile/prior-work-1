from flask import Blueprint, request
from app.services.middleware import validate_token
from app.services.category_service import *
from app.services.reviews_service import reviews_by_user
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository

category_repo = CategoryRepository()
user_repo = UserRepository()

category_bp = Blueprint('category_bp', __name__,  url_prefix='/categories')

@category_bp.route('', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        return get_all_categories()


@category_bp.route('/<category_id>', methods=['GET', 'PUT', 'DELETE'])
# @validate_token
def get_category(category_id):
    if request.method == 'GET':
        return get_one_category(category_id)
    elif request.method == 'PUT':
        return update_one_category(category_id)
    elif request.method == 'DELETE':
        return delete_one_category(category_id)

@category_bp.route('/<user_id>/category_list', methods=['GET'])
# @validate_token
def get_user_categories(user_id):
    return get_user_categories_list(user_id)


@category_bp.route('/<user_id>/add_category/<category>', methods=['POST'])
# @validate_token
def add_category(user_id, category):
    return add_user_category(user_id, category)


@category_bp.route('/<category_id>/add_site/<site_id>', methods=['POST'])
# @validate_token
def add_site_to_user_category(category_id, site_id):
    return add_site_to_category(category_id, site_id)


# @category_bp.route('/<user_id>/delete_category', methods=['DELETE'])
# # @validate_token
# def delete_user_category(user_id, category_id):
#     try:
#         logger.info("here")
#         user_data = get_one_user(user_id)
#         user = User(**user_data)
#         return user_repo.update(user_id, user_data)     
#     except Exception as e:
#         return e
    
@category_bp.route('/delete_all', methods=['DELETE'])
def delete_all_categories():
    return category_repo.delete_all_categories()
 

