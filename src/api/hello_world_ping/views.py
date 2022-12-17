from flask import Blueprint, make_response, jsonify, Response, request

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint

blueprint = Blueprint('hello_world_ping', __name__)


@blueprint.route(Endpoint.HELLO_WORLD, methods=[HttpMethod.GET])
def hello_world():
    return "Hello World"


@blueprint.route('/set-cookie', methods=['GET'])
def set_cookie():
    response = Response('You have set a cookie')
    response.set_cookie('id_token', 'somereallycoolvalue')

    return response


@blueprint.route('/get-cookie', methods=['GET'])
def get_cookie():
    cookie = request.cookies.get('id_token')

    if cookie is None:
        res = 'Cookie not set'
    else:
        res = f'Cookie: {cookie}'

    return res


@blueprint.route('/remove-cookie', methods=['GET'])
def remove_cookie():
    if request.cookies.get('id_token'):
        res = Response('id_token has been unset')
        res.delete_cookie('id_token')
    else:
        res = 'id_token was not a cookie'

    return res


def register_docs(docs):
    register_view(docs, blueprint, [
        hello_world
    ])
