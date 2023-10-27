from flask import abort
from app.repositories.user_action_repository import UserActionRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.user_repository import UserRepository
from app.services.points_system_service import getAction
from app.models.user_action_model import UserAction
from app.utils.logger import logger


site_repo = SiteRepository()
user_repo = UserRepository()
user_action_repo = UserActionRepository()



def getAllActions():
    return user_action_repo.findAll()

def getUserActions(user_id):
    user_actions = user_action_repo.findAllByField('user_id', user_id)
    if not user_actions:
        abort(404)
    return user_actions


def getPoints(action):
    points = getAction(action)['points']
    logger.info(points)
    
    if not points:
        abort(404)
    return points


def addSiteAction(user_id, site_id, action):
    logger.info(user_id)
    user_data = user_repo.findById(user_id)
    site_data = site_repo.findById(site_id)
    if not user_data or not site_data:
        abort(404)
    logger.info("1")

    points = getPoints(action)
    user_action_data = {
        "user_id": user_id,
        "site_id": site_id,
        "action": action  ,
        "points": points
    }
    logger.info(points)
    user_action = UserAction(**user_action_data)

    return user_action_repo.save(user_action)

def addUserAction(user_id, other_user_id, action):
    user_data = user_repo.findById(user_id)
    other_user_data = site_repo.findById(other_user_id)
    if not user_data or not other_user_data:
        abort(404)

    getPoints(action)
    user_action_data = {
        "user_id": user_id,
        "other_user_id": other_user_data,
        "action": action  
    }
    user_action = UserAction(**user_action_data)

    return user_action_repo.save(user_action)

def getScoreBreakdown(user_id):
    user_actions = getUserActions(user_id)
    # Dictionary to store total points for each action
    action_points = {}

    # Loop through the list of dictionaries and calculate total points for each action
    for action_dict in user_actions:
        if 'points' in action_dict:
            action_name = action_dict["action"]
            points = action_dict["points"]
            # If action_name is already in the dictionary, add points to the existing total
            # Otherwise, create a new entry in the dictionary
            if action_name in action_points:
                action_points[action_name] += points
            else:
                action_points[action_name] = points
    return action_points

