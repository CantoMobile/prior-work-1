from bson import ObjectId
from flask import abort, jsonify, request
import datetime
import json
from app.models import Referral
from app.models import User
from app.repositories.referrals_repository import ReferralsRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import create_user, add_user_role, remove_user_role
from app.utils.logger import logger


referrals_repo = ReferralsRepository()
user_repo = UserRepository()
auth = AuthService()


def get_all_referrals(page=None):
    if page is not None:
        referrals_data = referrals_repo.findAll(page, 15)
    else:
        referrals_data = referrals_repo.findAll()
    return referrals_data


def get_one_referral(referral_id):
    referral = referrals_repo.findById(referral_id)
    if not referral:
        abort(404)
    return referral


def find_referrals_by_referrer(user_id):
    referrals = referrals_repo.count({"referred_by":user_id})
    return jsonify({"referrals": referrals})


def find_referal_by_referred(user_id):
    referral = referrals_repo.findAllByField('referred_user_id', user_id)
    if not referral:
        return []
    return referral


def initiate_referral(referring_user_id):
    data = request.json 
    new_user = create_user(data, True)    
    user_id = new_user['user']['_id']
    add_user_role(user_id, "646c0099d72ed166e49c3890")
    referral = Referral(
            referred_by = referring_user_id,
            referred_user_id = user_id,
            referral_date = datetime.datetime.now(),
            referral_status = 'Complete'
        )
    try:
        referral_data = referrals_repo.save(referral)
        if referral_data != None:
            return new_user
    except Exception as e:
        return jsonify({"error": "Error initiating referral", "message": str(e)}), 400


def complete_referral(referral_id):
    referral_data = get_one_referral(referral_id)
    referral_data['referral_status'] = 'Complete'
    user_id = referral_data['referred_user_id']
    
    remove_user_role(user_id, "6509e07e309e42bea36ffcc7") # Remove Pending role
    add_user_role(user_id, "646c0099d72ed166e49c3890") # Add User role

    return referrals_repo.update(referral_id, referral_data)





