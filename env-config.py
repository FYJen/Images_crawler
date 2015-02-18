from db import db_config

class BasicConfig(object):
    SQLALCHEMY_DATABASE_URI = db_config.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_MIGRATE_REPO = db_config.SQLALCHEMY_MIGRATE_REPO

class Development(BasicConfig):
    DEVELOPMENT = True
    DEBUG = True

class Production(BasicConfig):
    DEBUG=False
