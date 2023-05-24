class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = "mongodb+srv://root:WQORfJaUG61PyvkA@test.tjj7n3c.mongodb.net/test"
    SECRET_KEY = "6x48Gq3Xe&guqF@ReV"

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = "mongodb+srv://root:WQORfJaUG61PyvkA@test.tjj7n3c.mongodb.net/test"
    SECRET_KEY = "KyQ$#J7mk&hJGL#$8v"
