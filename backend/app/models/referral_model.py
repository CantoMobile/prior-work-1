import datetime
from bson import ObjectId


class Referral:
    def __init__(self, referred_by, referred_user_id, referral_date, referral_status, _id = None):
        self.referred_by = referred_by
        self.referred_user_id = referred_user_id
        self.referral_date = referral_date
        self.referral_status = referral_status
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def serialize(self):
        return {
            'id': str(self._id),
            'referral_code': self.referral_code,
            'referred_by': self.referred_by,
            'referrals': self.referrals
        }