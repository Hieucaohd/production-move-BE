from flask import Blueprint

from src.api import HttpMethod
from src.common.utils.docs_register import register_view
from src.api.urls import Endpoint
from src.api.admin.controllers import AdminController

blueprint = Blueprint('login', __name__)


@blueprint.route(Endpoint.CREATE_MANUFACTURE_FACTORY, methods=[HttpMethod.POST])
def create_manufacture_factory():
    return AdminController.create_manufacture_factory()


@blueprint.route(Endpoint.CREATE_DISTRIBUTION_AGENT, methods=[HttpMethod.POST])
def create_distribution_agent():
    return AdminController.create_distribution_agent()


@blueprint.route(Endpoint.CREATE_WARRANTY_CENTER, methods=[HttpMethod.POST])
def create_warranty_center():
    return AdminController.create_warranty_center()


@blueprint.route(Endpoint.CREATE_PRODUCT_LINE, methods=[HttpMethod.POST])
def create_product_line():
    return AdminController.create_product_line()


@blueprint.route(Endpoint.CREATE_PRODUCTION_LOT, methods=[HttpMethod.POST])
def create_production_lot():
    return AdminController.create_production_lot()


@blueprint.route(Endpoint.EXPORT_PRODUCTION_LOT, methods=[HttpMethod.POST])
def export_production_lot():
    return AdminController.export_production_lot()


@blueprint.route(Endpoint.SOLD_PRODUCTION, methods=[HttpMethod.POST])
def sold_production():
    return AdminController.sold_production()


@blueprint.route(Endpoint.GUARANTEE_PRODUCTION, methods=[HttpMethod.POST])
def guarantee_production():
    return AdminController.guarantee_production()


@blueprint.route(Endpoint.GUARANTEE_DONE, methods=[HttpMethod.POST])
def guarantee_done():
    return AdminController.guarantee_done()


def register_docs(docs):
    register_view(docs, blueprint, [
        create_manufacture_factory,
        create_distribution_agent,
        create_warranty_center,
        create_product_line,
        create_production_lot,
        export_production_lot,
        sold_production,
        guarantee_production,
        guarantee_done,
    ])
