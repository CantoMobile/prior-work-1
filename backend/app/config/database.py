import os
from pymongo import MongoClient
import certifi

from app.utils.logger import logger
from .config import ProductionConfig, DevelopmentConfig

class Database:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if os.environ.get('FLASK_ENV') == 'development':
            uri = DevelopmentConfig.MONGO_URI
            self.env = "PreProduction"
        else:
            uri = ProductionConfig.MONGO_URI
            self.env = "Production"
        self.mongo_uri = uri
        self.client = None
        self.db = None

    def connect(self):
        if self.client is None:
            try:
                ca = certifi.where()
                self.client = MongoClient(self.mongo_uri, tlsCAfile=ca)
                self.db = self.client['test']
                logger.info("Connect successfully to Mongo {}!".format(self.env))
            except ConnectionError as e:
                logger.error("Error connecting to Mongo ", str(e))
        return self.db

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
