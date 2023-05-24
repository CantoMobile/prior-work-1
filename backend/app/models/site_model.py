from .site_stats_model import SiteStats


class Site:

    def __init__(self, url, name, description=None, keywords=None, media=None, admin_email=None, site_stats=None):
        self.url = url
        self.name = name
        self.description = description
        self.keywords = keywords or []
        self.media = media or []
        self.admin_email = admin_email
        self.site_stats = site_stats

    def serialize(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords,
            'media': self.media,
            'admin_email': self.admin_email,
            'site_stats': str(self.site_stats.id) if self.site_stats else None
    }
