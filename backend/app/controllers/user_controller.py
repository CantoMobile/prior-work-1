from flask import Blueprint, request
from app.services.middleware import validate_token
from app.services.user_service import *
from app.services.reviews_service import reviews_by_user
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.config.database import Database
from app.utils.logger import logger

category_repo = CategoryRepository()
user_repo = UserRepository()

user_bp = Blueprint('user_bp', __name__,  url_prefix='/users')


@user_bp.route('', methods=['GET', 'POST'])
# @validate_token
def users():
    if request.method == 'GET':
        return get_all_users()

    elif request.method == 'POST':
        data = request.json
        return get_all_users(data['page'])


@user_bp.route('/add_user', methods=['POST'])
@validate_token
def add_user():
    return create_user()


@user_bp.route('/register', methods=['POST'])
def user_registry():
    return create_user(True)


@user_bp.route('/<user_id>', methods=['GET', 'PUT', 'DELETE'])
# @validate_token
def user(user_id):
    if request.method == 'GET':
        return get_one_user(user_id)

    elif request.method == 'PUT':
        return update_one_user(user_id)

    elif request.method == 'DELETE':
        return delete_one_user(user_id)


@user_bp.route('/authentication', methods=['POST'])
def authentication():
    return user_authentication()


@user_bp.route('/<string:user_id>/set_password', methods=['PUT'])
@validate_token
def set_password(user_id):
    return set_user_password(user_id)


@user_bp.route('/<user_id>/add_role/<role_id>', methods=['PUT'])
@validate_token
def add_role(user_id, role_id):
    return add_user_role(user_id, role_id)


@user_bp.route('/<user_id>/remove_role/<role_id>', methods=['PUT'])
@validate_token
def remove_role(user_id, role_id):
    return remove_user_role(user_id, role_id)


@user_bp.route('/<user_id>/reviews', methods=['GET'])
@validate_token
def site_reviews(user_id):
    return reviews_by_user(user_id)


@user_bp.route('/<user_id>/save_site/<site_id>', methods=['PUT'])
@validate_token
def save_site(user_id, site_id):
    return save_site_user(user_id, site_id)

@user_bp.route('/<user_id>/remove_site/<site_id>', methods=['DELETE'])
# @validate_token
def remove_site(user_id, site_id):
    return remove_site_user(user_id, site_id)


user_data = [
    # User 1
    User(
        name="User 1",
        email="user1@example.com",
        password="password1",
        sites=['Amazon', 'eBay', 'CNN', 'TED', 'LinkedIn']
    ),

    # User 2
    User(
        name="User 2",
        email="user2@example.com",
        password="password2",
        sites=['Facebook', 'Twitter', 'LinkedIn', 'Indeed']
    ),

    # User 3
    User(
        name="User 3",
        email="user3@example.com",
        password="password3",
        sites=['Coursera', 'edX', 'Codecademy', 'Airbnb']
    ),

    # User 4
    User(
        name="User 4",
        email="user4@example.com",
        password="password4",
        sites=['WebMD', 'Healthline', 'MyFitnessPal', 'Men\'s Health', 'CNN']
    ),

    # User 5
    User(
        name="User 5",
        email="user5@example.com",
        password="password5",
        sites=['Bloomberg', 'Forbes', 'CNBC', 'The Wall Street Journal']
    ),

    # User 6
    User(
        name="User 6",
        email="user6@example.com",
        password="password6",
        sites=['Vogue', 'GQ', 'Refinery29', 'The Cut']
    ),

    # User 7
    User(
        name="User 7",
        email="user7@example.com",
        password="password7",
        sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer', 'LinkedIn']
    ),

    # User 8
    User(
        name="User 8",
        email="user8@example.com",
        password="password8",
        sites=['Spotify', 'Apple Music', 'Pandora', 'SoundCloud', 'Instagram']
    ),

    # User 9
    User(
        name="User 9",
        email="user9@example.com",
        password="password9",
        sites=['Indeed', 'LinkedIn', 'Glassdoor', 'Monster', 'CNN']
    ),

    # User 10
    User(
        name="User 10",
        email="user10@example.com",
        password="password10",
        sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 11
    User(
        name="User 11",
        email="user11@example.com",
        password="password11",
        sites=['IMDb', 'Rotten Tomatoes', 'Indeed', 'Entertainment Weekly']
    ),

    # User 12
    User(
        name="User 12",
        email="user12@example.com",
        password="password12",
        sites=['TechCrunch', 'The Verge', 'Wired', 'Gizmodo']
    ),

    # User 13
    User(
        name="User 13",
        email="user13@example.com",
        password="password13",
        sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'ESPN']
    ),

    # User 14
    User(
        name="User 14",
        email="user14@example.com",
        password="password14",
        sites=['ESPN', 'Sports Illustrated', 'Bleacher Report', 'CBS Sports']
    ),

    # User 15
    User(
        name="User 15",
        email="user15@example.com",
        password="password15",
        sites=['CNN', 'BBC News', 'The New York Times', 'Al Jazeera', 'Codecademy']
    ),

    # User 16
    User(
        name="User 16",
        email="user16@example.com",
        password="password16",
        sites=['Vogue', 'GQ', 'Refinery29', 'The Cut', 'ESPN']
    ),

    # User 17
    User(
        name="User 17",
        email="user17@example.com",
        password="password17",
        sites=['IGN', 'Polygon', 'Kotaku', 'PC Gamer', 'Al Jazeera']
    ),

    # User 18
    User(
        name="User 18",
        email="user18@example.com",
        password="password18",
        sites=['Spotify', 'Expedia', 'Pandora', 'Variety']
    ),

    # User 19
    User(
        name="User 19",
        email="user19@example.com",
        password="password19",
        sites=['Indeed', 'LinkedIn', 'Glassdoor', 'Monster', 'CNN', 'Codecademy', 'edX', 'IMDb', 'Expedia']
    ),

    # User 20
    User(
        name="User 20",
        email="user20@example.com",
        password="password20",
        sites=['TripAdvisor', 'Expedia', 'Airbnb', 'Lonely Planet']
    ),

    # User 21
    User(
        name="User 21",
        email="user21@example.com",
        password="password21",
        sites=['IMDb', 'TripAdvisor', 'Variety', 'Entertainment Weekly']
    ),

    # User 22
    User(
        name="User 22",
        email="user22@example.com",
        password="password22",
        sites=['TechCrunch', 'The Verge', 'Facebook']
    ),

    # User 23
    User(
        name="User 23",
        email="user23@example.com",
        password="password23",
        sites=['AllRecipes', 'Food Network', 'Bon Appétit', 'Instagram']
    ),

    # User 24
    User(
        name="User 24",
        email="user24@example.com",
        password="password24",
        sites=['ESPN', 'Sports Illustrated', 'Codecademy', 'TripAdvisor']
    ),

    # User 25
    User(
        name="User 25",
        email="user25@example.com",
        password="password25",
        sites=['edX', 'BBC News', 'The New York Times', 'Al Jazeera']
    ),

    # User 26
    User(
        name="User 26",
        email="user26@example.com",
        password="password26",
        sites=['Amazon', 'eBay', 'Facebook', 'Etsy']
    ),

    # User 27
    User(
        name="User 27",
        email="user27@example.com",
        password="password27",
        sites=['Facebook', 'Twitter', 'Etsy', 'Pinterest', 'Amazon', 'edX']
    ),

    # User 28
    User(
        name="User 28",
        email="user28@example.com",
        password="password28",
        sites=['Khan Academy', 'Coursera', 'edX', 'TED', 'WebMD', 'Forbes']
    ),

    # User 29
    User(
        name="User 29",
        email="user29@example.com",
        password="password29",
        sites=['Twitter', 'Healthline', 'MyFitnessPal', 'Mayo Clinic']
    ),

    # User 30
    User(
        name="User 30",
        email="user30@example.com",
        password="password30",
        sites=['Forbes', 'Instagram', 'CNBC', 'The Wall Street Journal', 'edX', 'CNN', 'IGN']
    ),

    # User 31
    User(
        name="User 31",
        email="user31@example.com",
        password="password30",
        sites=['IGN', 'Polygon', 'CNN', 'eBay', 'Amazon', 'Expedia']
    )

]


@user_bp.route('/insertMany', methods=['POST'])
def insertMany():
    _db = Database()
    logger.info("1")
    db = _db.connect()
    logger.info("2")

    # Step 4: Access the 'site_test_data' collection and insert the data
    

    try: 
        user_test_data_collection = db['user_test_data']
        # logger.info(user_test_data_collection)
        # logger.info([user.serialize() for user in user_data])
        # user_docs = [user.serialize() for user in user_data]
        # logger.info("4")
        # user_insert_result = user_test_data_collection.insert_many(user_docs)
        #logger.info(site_insert_result)
    except Exception as e:
        logger.info("3")
        return e
        

    return str(list(user_test_data_collection.find({"name": "User 1"})))



