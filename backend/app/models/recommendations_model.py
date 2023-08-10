

class Recommendation:
    def __init__(self, user_id, recommendations=None, _id=None):
        self.user_id = user_id
        self.recommendations = recommendations or {}
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def add_recommendation(self, site_id, score):
        self.recommendations[site_id] = score

    def serialize(self):
        return {
            'id': str(self._id),
            'user_id': self.user_id,
            'recommendations': self.recommendations
        }