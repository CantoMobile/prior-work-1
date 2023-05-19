from flask import abort, request
from models.site_stats_model import SiteStats
from bson.objectid import ObjectId
from repositories.abstract_repository import AbstractRepository
from main import db


class SiteStatsRepository(AbstractRepository[SiteStats]):
    pass