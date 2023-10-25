
class PointsSystem:
    def __init__(self, action, points, _id = None):
        self.action = action
        self.points = points
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def serialize(self):
        return {
            'id': str(self._id),
            'action': self.action,
            'points': self.points
        }