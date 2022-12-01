from flask import Blueprint

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint
from src.api.auth.controllers import AuthController

blueprint = Blueprint('auth', __name__)


@blueprint.route(Endpoint.LOGIN, methods=[HttpMethod.POST])
def login():
    return AuthController.login()


def register_docs(docs):
    register_view(docs, blueprint, [
        login
    ])