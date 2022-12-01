from flask import Flask

from src.api.extensions import cache, cors

from src.settings.settings import ProdConfig
from src.api.exceptions import InvalidUsage

from autotech_sdk.database.mongo import MongoDBInit

from src.api.hello_world_ping import views as hello_world_views
from src.api.auth import views as auth_views
from src.api.admin import views as admin_views
from flask_apispec import FlaskApiSpec


def create_app(config_object=ProdConfig):
    """An application factory."""

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    register_extensions(app)
    register_error_handlers(app)
    register_blueprints(app)

    MongoDBInit.init_app(app)

    docs = FlaskApiSpec(app)
    register_blueprint_for_docs(docs)
    return app


def register_extensions(app):
    """Register Flask extensions."""

    cache.init_app(app)
    cors.init_app(app)


def register_blueprint_for_docs(docs: FlaskApiSpec):
    hello_world_views.register_docs(docs)
    auth_views.register_docs(docs)
    admin_views.register_docs(docs)


def register_blueprints(app: Flask):
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')

    cors.init_app(hello_world_views.blueprint, origins=origins)
    cors.init_app(auth_views.blueprint, origins=origins)
    cors.init_app(admin_views.blueprint, origins=origins)

    app.register_blueprint(hello_world_views.blueprint)
    app.register_blueprint(auth_views.blueprint)
    app.register_blueprint(admin_views.blueprint)


def register_error_handlers(app: Flask):

    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(error_handler)
