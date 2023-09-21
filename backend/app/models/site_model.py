from .site_stats_model import SiteStats


class Site:

    def __init__(self, url, name, description=None, logo=None, keywords=None, media=None, admin_email=None, site_stats=None, _id=None):
        self.url = url
        self.name = name
        self.description = description
        self.logo = logo
        self.keywords = keywords or []
        self.media = media or []
        self.admin_email = admin_email
        self.site_stats = site_stats if site_stats is not None else {"saves": 0}
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id

    def serialize(self):
        return {
            'id': str(self._id),
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'logo': self.logo,
            'keywords': self.keywords,
            'media': self.media,
            'admin_email': self.admin_email,
            'site_stats': self.site_stats
        }
