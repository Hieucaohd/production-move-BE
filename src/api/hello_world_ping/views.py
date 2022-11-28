from flask import Blueprint

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint

blueprint = Blueprint('hello_world_ping', __name__)


@blueprint.route(Endpoint.HELLO_WORLD, methods=[HttpMethod.GET])
def hello_world():
    return "Hello world"


def register_docs(docs):
    register_view(docs, blueprint, [
        hello_world
    ])
