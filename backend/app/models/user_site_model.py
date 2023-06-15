class UserSite:

    def __init__(self, user_id, site=None, _id=None):
        self.user_id = user_id
        if site != None: 
            self.site = site
        else: 
            self.site = []
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

