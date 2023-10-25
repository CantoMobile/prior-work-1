from flask import Blueprint, request

from app.services.referrals_service import *

referrals_bp = Blueprint('referrals_bp', __name__, url_prefix='/referrals')


@referrals_bp.route('', methods=['GET'])
def get_referrals():
    if request.method == 'GET':
        return get_all_referrals()
    elif request.method == 'POST':
        data = request.json
        return get_all_referrals(data['page'])
    

@referrals_bp.route('/<referral_id>', methods=['GET'])
def get_referral(referral_id):
    return get_one_referral(referral_id)

@referrals_bp.route('/<referral_id>/referreds', methods=['GET'])
def get_referreds_count(referral_id):
    return find_referrals_by_referrer(referral_id)



@referrals_bp.route('/<referring_user_id>/initiate_referral', methods=['POST'])
def begin_referral(referring_user_id):
    return initiate_referral(referring_user_id)


#IMPORTANT
@referrals_bp.route('/<referral_id>/complete_referral', methods=['PUT'])
def confirm_referral(referral_id):
    return complete_referral(referral_id)
