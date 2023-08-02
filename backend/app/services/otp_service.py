import datetime
from os import abort
from bson import ObjectId
from flask import request, jsonify
from app.repositories.otp_repository import OtpRepository
from app.models.otp_model import Otp
from app.utils.email_helper import send_otp_email
otp_repo = OtpRepository()


def add_one_otp(data=None):
    if data is None:
        data = request.json
    if 'user_id' not in data:
        abort(401)
    otp = Otp(user_id=data['user_id'],
              site_url=data['site_url'])
    old_otp = otp_repo.findByField('site_url', data['site_url'])
    if not old_otp:
        old_otp = otp_repo.findByField('user_id', data['user_id'])
    if old_otp:
        otp_repo.delete(old_otp['_id'])
    otp_data = otp_repo.save(otp)
    if send_otp_email(data['email'], otp_data['otp']):
        return otp_data
    else:
        return None


def delete_one_otp(otp_id):
    if otp_repo.existsByField('_id', ObjectId(otp_id)):
        return otp_repo.delete(otp_id)
    else:
        print("Not is possible to delete otp_code")
        return jsonify({"Error": "Not is possible to delete otp_code"}), 401


def get_one_otp(user_id, otp_code):
    otp_data = otp_repo.findByField('user_id', user_id)
    if otp_data:
        if otp_data['otp'] == otp_code:
            return otp_data
    else:
        return None


def validate_otp_code(user_id, otp_code):
    otp_data = get_one_otp(user_id, otp_code)
    print("optdata:", otp_data)
    if otp_data:
        if otp_data['expiration_time'] > datetime.datetime.now():
            delete_one_otp(otp_data['_id'])
            return True
    else:
        return False
