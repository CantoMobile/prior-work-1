import datetime
import random
import string


class Otp:

    def __init__(self, user_id, site_url=None, otp=None,expiration_time=None, _id=None):
        self.user_id = user_id
        if otp is None:
            self.otp = self.generate_otp()
        else: self.otp = otp
        self.site_url = site_url or None
        if expiration_time is None: 
            self.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
        else: 
            self.expiration_time = expiration_time
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    @staticmethod
    def generate_otp(length=6):
            characters = string.digits
            otp = ''.join(random.choice(characters) for _ in range(length))
            return otp