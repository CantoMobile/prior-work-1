from datetime import datetime


class SiteStats:

    def __init__(self, site, visits=0, unique_visitors=0, last_visit=None, _id=None):
        self.site = site
        self.visits = visits
        self.unique_visitors = unique_visitors
        if last_visit is None:
            self.last_visit = datetime.now()
        else:
            self.last_visit = last_visit
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id
