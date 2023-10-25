from flask import jsonify, request, abort
from app.repositories.points_system_repository import PointsSystemRepository
from app.models.points_system_model import PointsSystem
from app.utils.logger import logger

points_system_repo = PointsSystemRepository()

def getAllActions():
    return points_system_repo.findAll()

def getAction(action):
    action = points_system_repo.findByField('action', action)
    if not action:
        return False
    return action

def addActions():
    data = request.json

    actions = data['actions']
    # Insert each action into the scoring_system collection
    for action in actions:
        action_name = action['action']
        points = action['points']

        if not getAction(action_name):
            action_data = {
                'action': action_name, 
                'points': points
            }
            action = PointsSystem(**action_data)
            points_system_repo.save(action)
        
        continue
    
    return jsonify({'message': 'Actions added successfully!'})


def deleteAction():
    data = request.json

    action_name = data['action']
    action_data = getAction(action_name)

    if 'points' in data:
        action_data['points'] = data['points']
        return points_system_repo.deleteByField('action', action_name)
    else:
        return jsonify({'message': 'This action does not exist'})
    

def updateAction(action_id):
    data = request.json

    action_name = data['action']
    action_data = getAction(action_name)

    if not action_data:
        return jsonify({'message': 'This action does not exist'})
    
    if 'points' in data:
        action_data['points'] = data['points']
    
    return points_system_repo.update(action_id, action_data)

