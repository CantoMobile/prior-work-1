from flask import abort, request
from app.models.otp_model import Otp
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class OtpRepository(AbstractRepository[Otp]):
    pass
