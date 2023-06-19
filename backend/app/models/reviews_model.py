import datetime
from bson import ObjectId


class Review:
    def __init__(self, site_id, user_id, rating, comment, created_at=None, _id=None):
        self.site_id = site_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
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
            'site_id': self.site_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
