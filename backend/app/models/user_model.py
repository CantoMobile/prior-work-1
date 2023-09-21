import datetime
from bson import ObjectId


class User:
    def __init__(self, name, email, password, referral_code, referrals=None, auth_provider=None, sites=None, role=None, isAdmin=None, created_at=None, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self.referral_code = referral_code
        self.referrals = referrals or []
        self.auth_provider = auth_provider
        self.sites = sites or {}
        self.role = role  # or []
        self.isAdmin = isAdmin if isAdmin else False
        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at
            
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def verify_password(self, password):
        return self.password == password

    def set_password(self, password):
        if self.password == password:
            return None
        elif len(password) > 10:
            self.password = password
            return True
        else:
            return False

    # def serialize(self):
    #     return {
    #         'name': self.name,
    #         'email': self.email,
    #         'password': self.password,
    #         'sites': self.sites,
    #         'created_at': self.created_at
    # }

