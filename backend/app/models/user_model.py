import datetime
from bson import ObjectId


class User:
    def __init__(self, name, email, password, sites=None, role=None, isAdmin=None, isGoogle=None,  uidGoogle=None,  created_at=None, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self.sites = sites or []
        self.role = role  
        self.isAdmin = isAdmin if isAdmin else False
        self.isGoogle = isGoogle if isGoogle else False
        self.uidGoogle = uidGoogle if uidGoogle else None
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


    # def serialize(self):
    #     return {
    #         'name': self.name,
    #         'email': self.email,
    #         'password': self.password,
    #         'sites': self.sites,
    #         'created_at': self.created_at
    # }

