from flask import abort, request
from app.models.site_stats_model import SiteStats
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class SiteStatsRepository(AbstractRepository[SiteStats]):
    pass