import os


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    TESTING = False


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    DATABASE_URI = "postgresql://localhost:5432/crypto_prod_db"


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URI = "postgresql://localhost:5432/crypto_dev_db"


class TestConfig(Config):
    ENV = "test"
    TESTING = True
    DATABASE_URI = "postgresql://localhost:5432/crypto_test_db"
