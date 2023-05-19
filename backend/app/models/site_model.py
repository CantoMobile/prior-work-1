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
