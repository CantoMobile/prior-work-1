import datetime

class UserAction:

    def __init__(self, user_id, action, site_id=None, other_user_id=None, completed_at=None, _id=None):
        self.user_id = user_id
        self.action = action
        self.site_id = site_id
        self.other_user_id = other_user_id
        if completed_at is None:
            self.completed_at = datetime.datetime.now()
        else:
            self.completed_at = completed_at
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id