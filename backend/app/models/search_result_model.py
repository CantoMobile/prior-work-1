from .site_model import Site


class SearchResult:

    def __init__(self, query_string, results=None, site=None):
        self.query_string = query_string
        self.results = results or []
        self.site = site

