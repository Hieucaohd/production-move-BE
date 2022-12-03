from flask import Blueprint, request

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


@blueprint.route(Endpoint.ALL_PRODUCT_LINES, methods=[HttpMethod.GET])
def get_all_product_lines():
    return AdminController.get_product_lines()


@blueprint.route(Endpoint.ALL_MANUFACTURE_FACTORIES, methods=[HttpMethod.GET])
def get_all_manufacture_factories():
    return AdminController.get_manufacture_factories()


@blueprint.route(Endpoint.ALL_DISTRIBUTION_AGENTS, methods=[HttpMethod.GET])
def get_all_distribution_agents():
    return AdminController.get_distribution_agents()


@blueprint.route(Endpoint.ALL_WARRANTY_CENTERS, methods=[HttpMethod.GET])
def get_all_warranty_centers():
    return AdminController.get_warranty_centers()


@blueprint.route(Endpoint.ALL_PRODUCTIONS, methods=[HttpMethod.GET])
def get_all_productions():
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)
    return AdminController.get_all_productions(page, per_page)


@blueprint.route(Endpoint.ALL_PRODUCTION_LOTS, methods=[HttpMethod.GET])
def get_all_production_lots():
    return AdminController.get_all_production_lots()


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
