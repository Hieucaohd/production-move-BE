from flask import Blueprint

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint
from src.api.auth.controllers import AuthController
from flask_cors import cross_origin

blueprint = Blueprint('auth', __name__)


@blueprint.route(Endpoint.LOGIN, methods=[HttpMethod.POST])
@cross_origin(supports_credentials=True)
def login():
    return AuthController.login()


@blueprint.route(Endpoint.LOGOUT, methods=[HttpMethod.POST])
def logout():
    return AuthController.logout()


def register_docs(docs):
    register_view(docs, blueprint, [
        login
    ])