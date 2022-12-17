from flask import Blueprint, make_response, jsonify

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint

blueprint = Blueprint('hello_world_ping', __name__)


@blueprint.route(Endpoint.HELLO_WORLD, methods=[HttpMethod.GET])
def hello_world():
    response = make_response("Hello world")
    response.set_cookie("my_fisrt_cookie", "valuehhhh", samesite=None)
    return response


@blueprint.route("/test-cookie", methods=[HttpMethod.GET])
def test_cookie():
    response = jsonify({
        "hello": "world"
    })
    response.set_cookie("test_cookie", value="hello")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def register_docs(docs):
    register_view(docs, blueprint, [
        hello_world
    ])
