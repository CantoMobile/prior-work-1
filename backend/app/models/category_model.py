import datetime

class Category:
    def __init__(self, name, user_id, sites=None, created_at=None, _id=None):
        self.name = name
        self.sites = sites or []
        self.user_id = user_id
        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'sites': self.sites,
            'user_id': self.user_id,
            'created_at': self.created_at
        }