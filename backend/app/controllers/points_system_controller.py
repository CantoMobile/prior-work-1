from flask import Blueprint, jsonify, request, abort
from app.repositories.points_system_repository import PointsSystemRepository
from app.models.points_system_model import PointsSystem
from app.services.points_system_service import *
from app.utils.logger import logger

points_system_repo = PointsSystemRepository()

points_system_bp = Blueprint('points_system_bp', __name__, url_prefix='/points_system')

@points_system_bp.route('/', methods=['GET'])
def get_actions():
    return getAllActions

@points_system_bp.route('/add_actions', methods=['POST'])
def add_actions():
    return addActions()

@points_system_bp.route('/delete_action', methods=['DELETE'])
def delete_action():
    return deleteAction()

@points_system_bp.route('/<action_id>', methods=['PUT'])
def update_action(action_id):
    return updateAction(action_id)

