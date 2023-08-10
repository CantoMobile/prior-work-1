from flask import Blueprint, Response
from app.services.user_site_service import return_not_referenced, return_referenced
from app.services.middleware import admin_permission_required
from app.services.site_service import *
from app.services.user_service import add_created_site_user
from app.config.database import Database
import numpy as np


site_bp = Blueprint('site_bp', __name__, url_prefix='/sites')


@site_bp.route('', methods=['GET'])
def sites():
    if request.method == 'POST':
        data = request.json
        return get_all_sites(data['page'])
    elif request.method == 'GET':
        return get_all_sites()


@site_bp.route('/add_site', methods=['POST'])
def add_site():
    return create_site()


@site_bp.route('/<site_id>', methods=['GET', 'PUT', 'DELETE'])
# @admin_permission_required
def site(site_id):
    if request.method == 'GET':
        return get_one_site(site_id)

    elif request.method == 'PUT':
        return update_one_site(site_id)

    elif request.method == 'DELETE':
        return delete_one_site(site_id)


@site_bp.route('/<user_id>/search', methods=['GET', 'POST'])
def search_sites(user_id):
    if request.method == 'GET':
        return search_sites_logged(user_id)
    elif request.method == 'POST':
        data = request.json
        return search_sites_logged(user_id, data['page'])


@site_bp.route('/<user_id>/search_saves', methods=['GET', 'POST'])
def search_sites_saves(user_id):
    if request.method == 'GET':
        return search_sites_saves_logged(user_id)
    elif request.method == 'POST':
        data = request.json
        return search_sites_saves_logged(user_id, data['page'])


@site_bp.route('/search', methods=['GET'])
def search_sites_logout():
    return search_sites_not_logged()


@site_bp.route('/search_suggested', methods=['GET'])
def search_sites_suggested():
    return search_sites_name_suggested()


@site_bp.route('/<site_id>/stats', methods=['GET'])
def site_stats(site_id):
    return stats_by_site(site_id)


@site_bp.route('/not_user/<user_id>', methods=['GET'])
def get_sites_not_ref_by_user(user_id):
    return return_not_referenced(user_id)


@site_bp.route('/user/<user_id>', methods=['GET'])
def get_sites__ref_by_user(user_id):
    response_data = jsonify(return_referenced(user_id))

    response = Response(response_data, content_type='application/json')
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day

    return response


@site_bp.route('/top6_saved', methods=['GET'])
def search_top_six_sites():
    return get_top_six_saved()


@site_bp.route('/<user_id>/save_site/<site_id>', methods=['PUT'])
def save_site(user_id, site_id):
    return add_created_site_user(site_id, user_id)



import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from app.utils.logger import logger
from app.repositories.site_repository import SiteRepository
from app.repositories.reviews_repository import ReviewsRepository
from app.repositories.user_repository import UserRepository
from app.repositories.category_repository import CategoryRepository
from app.config.database import Database  # Assuming you have a Database class to handle MongoDB connections

site_repo = SiteRepository()
reviews_repo = ReviewsRepository()
user_repo = UserRepository()
category_repo = CategoryRepository()


# Step 1: Preprocess the Data

# Function to preprocess text data
def preprocess_text(text):
    # Implement your text preprocessing techniques here
    return text


# Step 2: Similar Sites

# Function to calculate similarity between sites
def calculate_site_similarity(site_vectors):
    similarity_matrix = cosine_similarity(site_vectors)
    return similarity_matrix


# Step 4: Hybrid Approach

def merge_recommendations(similar_sites, similar_users, user_id):
    merged_recommendations = {}

    # Merge similar sites and similar users recommendations with equal weighting
    for site_id, similarity_score in enumerate(similar_sites):
        merged_recommendations[('site', site_id)] = 0.5 * similarity_score
    
    for user_id, similarity_score in enumerate(similar_users):
        merged_recommendations[('user', user_id)] = merged_recommendations.get(('user', user_id), 0) + 0.5 * similarity_score

    # Sort the merged recommendations in descending order based on the merged score
    sorted_recommendations = sorted(merged_recommendations.items(), key=lambda x: x[1], reverse=True)

    # Return the merged recommendations as a list of tuples with user/site IDs and merged scores
    return sorted_recommendations


def get_user_recommendations(user_id):
    # Main script
    _db = Database()
    db = _db.connect()
    test_site_repo = db['site_test_data']
    # Collect site 
    site_data = []
    for site_doc in list(test_site_repo.find()):
        site_data.append({
            'site_id': str(site_doc['_id']),
            'keywords': preprocess_text(site_doc['keywords']),
            'description': preprocess_text(site_doc['description']),
            'reviews': [review['comment'] for review in reviews_repo.query({'site_id': site_doc['_id']})]
        })
    # Collect user data
    test_user_repo = db['user_test_data']
    user_data = []
    user_id_to_index = {}  # Mapping of user_id to index
    index = 0
    for user_doc in list(test_user_repo.find()):
        user_sites = [site for category in category_repo.query({'user_id': user_doc['_id']}) for site in category['sites']]
        user_data.append({
            'user_id': str(user_doc['_id']),
            'saved_sites': [site for site in user_sites]
        })
        user_id_to_index[str(user_doc['_id'])] = index
        index += 1

    def calculate_user_similarity(user_matrix, user_data):
        normalized_user_matrix = normalize(user_matrix, axis=1)
        similarity_matrix = normalized_user_matrix.dot(normalized_user_matrix.T)
        logger.info(f'1: {similarity_matrix}')
        
        # Store user IDs and their similarity scores in a list of tuples
        user_similarities = [(user_data[i]['user_id'], similarity_matrix[user_id_to_index[user_data[i]['user_id']]]) for i in range(len(user_data))]
        logger.info(f'2: {user_similarities}')

        return similarity_matrix, user_similarities

    # Step 1: Preprocess the Data
    # Create TF-IDF vectorizer for site keywords, descriptions, and reviews
    vectorizer = TfidfVectorizer()
    site_texts = [str(site['keywords']) + ' ' + site['description'] + ' '.join(site['reviews']) for site in site_data]
    site_vectors = vectorizer.fit_transform(site_texts)

    # Step 2: Similar Sites

    # Calculate similarity matrix between sites
    site_similarity_matrix = calculate_site_similarity(site_vectors)

    # Get the feature names from the TF-IDF vectorizer
    feature_names = vectorizer.get_feature_names_out()

    # Step 3: Similar Users
    # Create user-site matrix
    user_site_matrix = []
    for user in user_data:
        user_vector = [1 if site_id in user['saved_sites'] else 0 for site_id in feature_names]
        user_site_matrix.append(user_vector)
    user_site_matrix = normalize(user_site_matrix, axis=1)

    # Calculate similarity matrix between users
    # Calculate similarity matrix between users and store user similarities
    user_similarity_matrix, user_similarities = calculate_user_similarity(user_site_matrix, user_data)

    # Step 4: Hybrid Approach

    # Iterate over users and provide recommendations
    similar_users = user_similarity_matrix[user_id_to_index[user_id]]
    # Check if 'user['saved_sites']' is empty before indexing the 'site_similarity_matrix'
    if user_data[user_id_to_index[user_id]]['saved_sites']:
        # Convert 'user['saved_sites']' to integers if it's not empty
        saved_site_indices = np.array(user_data[user_id_to_index[user_id]]['saved_sites']).astype(int)
        # Calculate the recommendation scores based on similar sites and similar users
        similar_sites = site_similarity_matrix[saved_site_indices].sum(axis=0)
    else:
        # If 'user['saved_sites']' is empty, assign similar_sites as an array of zeros
        similar_sites = np.zeros_like(site_similarity_matrix[user_id_to_index[user_id]])

    merged_recommendations = merge_recommendations(similar_sites, similar_users, user_id)

    # Process the merged recommendations and store them or use them as needed
    # Get the user and site IDs for the merged recommendations
    user_ids = [user_data[i]['user_id'] for i in range(len(user_data))]
    site_ids = [site['site_id'] for site in site_data]

    # Process the merged recommendations to obtain the actual recommendations
    actual_recommendations = []
    for recommendation, score in merged_recommendations:
        recommendation_type, id_value = recommendation
        if recommendation_type == 'user':
            user_id = user_ids[id_value]
            actual_recommendations.append((user_id, None, score))  # None for site ID since it's a user recommendation
        elif recommendation_type == 'site':
            site_id = site_ids[id_value]
            actual_recommendations.append((None, site_id, score))  # None for user ID since it's a site recommendation

    logger.info("2")
    # ... (Remaining code)

    # Process the merged recommendations and store them or use them as needed
    return actual_recommendations


@site_bp.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    db = Database()
    return get_user_recommendations(user_id)


@site_bp.route('/insertMany', methods=['POST'])
def insertMany():
    return "hello"
    # _db = Database()
    # logger.info("1")
    # db = _db.connect()
    # logger.info("2")

    # # Step 4: Access the 'site_test_data' collection and insert the data
    

    # try: 
    #     site_test_data_collection = db['site_test_data']
    #     logger.info(site_test_data_collection)
    #     logger.info([site.serialize() for site in site_data])
    #     site_docs = [site.serialize() for site in site_data]
    #     logger.info("4")
    #     site_insert_result = site_test_data_collection.insert_many(site_docs)
    #     #logger.info(site_insert_result)
    # except Exception as e:
    #     logger.info("3")
    #     return e
        
    # logger.info("5")
    # return str(list(site_test_data_collection.find()))

