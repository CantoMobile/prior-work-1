from bson import ObjectId
from flask import abort, jsonify, request
from app.repositories.category_repository import CategoryRepository
from app.models.category_model import Category
from app.utils.logger import logger


category_repo = CategoryRepository()


def add_user_category(user_id, category_name):
    category = Category(
        category_name,
        user_id
    )
    user_categories = category_repo.findAllByField('user_id', user_id)
    validation = any(
        category_item['name'] == category_name for category_item in user_categories)
    if validation:
        logger.info("here")
        return jsonify({'Error': 'The user already has this category'}), 304
    else:
        try:
            category_data = category_repo.save(category)
            return jsonify(category_data)
        except Exception as e:
            return jsonify({"error": "Error saving category",
                            "message": str(e)}), 400


def get_one_category(category_id):
    category = category_repo.findById(category_id)
    if not category:
        abort(404)
    return category


def update_one_category(category_id):
    category_data = get_one_category(category_id)
    data = request.json
    if 'name' in data:
        category_data['name'] = data['name']
    return category_repo.update(category_id, category_data)

def delete_one_category(category_id):
    if category_repo.existsByField('_id', ObjectId(category_id)):
        return category_repo.delete(category_id)
    else:
        return jsonify({'message': 'This category does not exist'}), 304


def get_user_categories_list(user_id):
    try:
        categories = category_repo.findAllByField('user_id', user_id)
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 401


def get_all_categories(page=None):
    logger.info(category_repo.findAll())
    try: 
        categories_data = category_repo.findAll()
    except Exception as e:
        return e
    return categories_data


def add_site_to_category(category_id, site_id):
    category_data = get_one_category(category_id)
    category = Category(**category_data)
    logger.info(category)
    validation = any(
        site_item == site_id for site_item in category.sites)
    logger.info(validation)
    if validation: 
        return {'Error': 'The user already has this site saved'}, 304
    else:
        logger.info(category_data['sites'])
        category_data['sites'].append(site_id)
        return category_repo.update(category_id, category_data)