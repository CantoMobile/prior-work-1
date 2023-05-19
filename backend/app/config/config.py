class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = "mongodb+srv://root:WQORfJaUG61PyvkA@test.tjj7n3c.mongodb.net/test"


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = "mongodb+srv://root:WQORfJaUG61PyvkA@test.tjj7n3c.mongodb.net/test"
