from flask import Blueprint, request
from app.services.user_action_service import *

user_actions_bp = Blueprint('user_actions_bp', __name__, url_prefix='/user_actions')


# @user_actions_bp.route('/<user_action_id>', methods=['GET', 'DELETE'])
# def user_site(relationship_id):
#     if request.method == 'GET':
#         return get_one_user_site(relationship_id)

#     elif request.method == 'DELETE':
#         return delete_one_user_site(relationship_id)


# @user_actions_bp.route('', methods=['GET', 'POST'])
# def user_sites():
#     if request.method == 'GET':
#         return get_all_user_sites()

#     elif request.method == 'POST':
#         data = request.json
#         return get_all_user_sites(data['page'])


@user_actions_bp.route('/', methods=['GET'])
def get_user_actions():
    return getAllActions()

@user_actions_bp.route('/<user_id>/add_site_action/<site_id>', methods=['POST'])
def add_site_action(user_id, site_id):
    action = request.json['action']
    return addSiteAction(user_id, site_id, action)

@user_actions_bp.route('/<user_id>/add_user_action/<other_user_id>', methods=['POST'])
def add_user_action(user_id, other_user_id):
    action = request.json['action']
    return addUserAction(user_id, other_user_id, action)

@user_actions_bp.route('/score_breakdown/<user_id>', methods=['GET'])
# @validate_token
def get_user_score_breakdown(user_id):
    return getScoreBreakdown(user_id)

