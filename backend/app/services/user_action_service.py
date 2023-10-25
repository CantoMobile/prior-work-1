from flask import abort
from app.repositories.user_action_repository import UserActionRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.user_repository import UserRepository
from app.models.user_action_model import UserAction
from app.utils.logger import logger


site_repo = SiteRepository()
user_repo = UserRepository()
user_action_repo = UserActionRepository()


def addScore(user_data, action):
    logger.info(user_data['score'])
    logger.info(type(user_data['score']))
    if action == 'Adding Your Site':
        user_data['score'] += 200
    elif action == 'Indexing New Site':
        user_data['score'] += 100
    elif action == 'Refer New User':
        user_data['score'] += 100
    elif action == 'Adding Logo':
        user_data['score'] += 50
    elif action == 'Adding Screenshot':
        user_data['score'] += 25
    
    return user_repo.update(user_data['_id'], user_data)


def addSiteAction(user_id, site_id, action):
    logger.info(user_id)
    user_data = user_repo.findById(user_id)
    site_data = site_repo.findById(site_id)
    if not user_data or not site_data:
        abort(404)
    logger.info("1")

    result = addScore(user_data, action)
    user_action_data = {
        "user_id": user_id,
        "site_id": site_id,
        "action": action  
    }
    logger.info(result)
    user_action = UserAction(**user_action_data)

    return user_action_repo.save(user_action)

def addUserAction(user_id, other_user_id, action):
    user_data = user_repo.findById(user_id)
    other_user_data = site_repo.findById(other_user_id)
    if not user_data or not other_user_data:
        abort(404)

    addScore(user_data, action)
    user_action_data = {
        "user_id": user_id,
        "other_user_id": other_user_data,
        "action": action  
    }
    user_action = UserAction(**user_action_data)

    return user_action_repo.save(user_action)

