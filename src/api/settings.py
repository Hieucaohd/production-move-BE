"""Application configuration."""
import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('URL_BUILDER_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))   # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = "simple"   # Can be "memcached", "redis", etc.
    CORS_ORIGIN_WHITELIST = []


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "prodDB")
    }


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'devDB'
    DB_PATH = None
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "devDB")
    }

    APISPEC_SPEC = APISpec(
        title='url-builder-docs',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0'
    )
    APISPEC_SWAGGER_URL = '/docs-json'
    APISPEC_SWAGGER_UI_URL = '/docs'

    CACHE_TYPE = 'simple'   # Can be "memcached", "redis", etc


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "testDB")
    }
