import os
from pymongo import MongoClient
import certifi
from .config import ProductionConfig, DevelopmentConfig

ca = certifi.where()
if os.environ.get('FLASK_ENV') == 'development':
    uri = DevelopmentConfig.MONGO_URI
    env = "PreProduction"
else:
    uri = ProductionConfig.MONGO_URI
    env = "Production"


def connect():
    try:
        client = MongoClient(uri, tlsCAfile=ca)
        db = client['test']
        print("You successfully connected to MongoDB {}!".format(env))
    except ConnectionError as e:
        print(e)
    return db
