import datetime
from bson import ObjectId


class User:
    def __init__(self, name, email, password, auth_provider=None, sites=None, role=None, created_at=None, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self.auth_provider = auth_provider
        self.sites = sites or []
        self.role = role  # or []
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
