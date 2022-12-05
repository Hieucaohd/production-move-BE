from src.api.auth.models import \
    ManufactureFactory, \
    ManufactureFactoryModel, \
    DistributionAgent, \
    DistributionAgentModel, \
    WarrantyCenter, \
    WarrantyCenterModel, \
    UserType
from src.api.auth.controllers import USER_AUTH_DATA_KEY, UserAuthData
from src.api.admin.forms import \
    CreateManufactureFactoryForm, \
    CreateDistributionAgentForm, \
    CreateWarrantyCenterForm, \
    CreateProductLineForm, \
    CreateProductionLotForm, \
    ExportProductionLotForm, SoldProductionForm, GuaranteeProductionForm, GuaranteeDoneForm, WarrantySendBackFactoryForm
from src.api.admin.models import \
    ProductLine, \
    ProductLineModel, \
    ProductionLot, \
    ProductionLotModel, \
    Production, \
    ProductionModel, \
    ProductionStatus, \
    DistributionAgentWarehouseModel, CustomerModel, Customer, GuaranteeHistory, GuaranteeHistoryModel
from flask import request, jsonify
from src.common.utils import generate_uuid
from datetime import datetime
from json import loads
import typing
from dacite import from_dict


class AdminController:
    @classmethod
    def create_manufacture_factory(cls):
        create_manufacture_factory_form: CreateManufactureFactoryForm = request.json
        data_to_create_manufacture_factory: ManufactureFactory = {
            **create_manufacture_factory_form,
            "manufacture_factory_id": generate_uuid(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        try:
            ManufactureFactoryModel.create_manufacture_factory(
                data_to_create_manufacture_factory)
            return jsonify({
                "manufacture_factory_id": data_to_create_manufacture_factory['manufacture_factory_id']
            })
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def create_distribution_agent(cls):
        create_distribution_agent_form: CreateDistributionAgentForm = request.json
        data_to_create_distribution_agent: DistributionAgent = {
            **create_distribution_agent_form,
            "distribution_agent_id": generate_uuid(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        try:
            DistributionAgentModel.create_distribution_agent(
                data_to_create_distribution_agent)
            return jsonify({
                "distribution_agent_id": data_to_create_distribution_agent["distribution_agent_id"]
            })
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def create_warranty_center(cls):
        create_warranty_center_form: CreateWarrantyCenterForm = request.json
        data_to_create_warranty_center: WarrantyCenter = {
            **create_warranty_center_form,
            "warranty_center_id": generate_uuid(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            'is_active': True
        }
        try:
            WarrantyCenterModel.create_warranty_center(
                data_to_create_warranty_center)
            return jsonify({
                "warranty_center_id": data_to_create_warranty_center['warranty_center_id']
            })
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def create_product_line(cls):
        create_product_line_form: CreateProductLineForm = request.json
        data_to_create_product_line: ProductLine = {
            **create_product_line_form,
            "product_line_id": generate_uuid(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        try:
            ProductLineModel.create_product_line(
                data_to_create_product_line)
            return jsonify({
                "product_line_id": data_to_create_product_line['product_line_id']
            })
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def create_production_lot(cls):
        create_production_lot_form = from_dict(CreateProductionLotForm, request.json)
        manufacture_factory: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY))

        if manufacture_factory["user_type"] != UserType.MANUFACTURE_FACTORY:
            return jsonify({"error": "User isn't manufacture factory"})

        productions: typing.List[Production] = []
        product_lot_id = generate_uuid()
        for _ in range(create_production_lot_form.production_number):
            production: Production = {
                "production_id": generate_uuid(),
                "product_lot_id": product_lot_id,
                'status': ProductionStatus.NEW_PRODUCTION
            }
            productions.append(production)

        try:
            ProductionModel.create_many_productions(productions)
        except Exception as er:
            return jsonify({"error": str(er)})

        data_to_create_production_lot: ProductionLot = {
            **create_production_lot_form.__dict__,
            "product_lot_id": product_lot_id,
            "manufacture_factory_id": manufacture_factory["id"]
        }

        try:
            ProductionLotModel.create_production_lot(
                data_to_create_production_lot)
            return jsonify({
                "product_lot_id": product_lot_id,
                "production_ids": [production['production_id'] for production in productions]
            })
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def export_production_lot(cls):
        export_production_lot_form = from_dict(ExportProductionLotForm, request.json)
        product_lot_id = export_production_lot_form.product_lot_id
        distribution_agent_id = export_production_lot_form.distribution_agent_id
        export_time = export_production_lot_form.export_time

        try:
            ProductionModel.change_many_productions_status(
                query={"product_lot_id": product_lot_id},
                status=ProductionStatus.GO_TO_DISTRIBUTION
            )
            ProductionLotModel.export_production_lot(
                product_lot_id=product_lot_id, distribution_agent_id=distribution_agent_id, export_time=export_time)

            DistributionAgentWarehouseModel.import_production_lot(product_lot_id, distribution_agent_id)
            return jsonify({"export_success": True})
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def sold_production(cls):
        sold_production_form: SoldProductionForm = from_dict(SoldProductionForm, request.json)

        try:
            DistributionAgentWarehouseModel.sold_production(
                production_id=sold_production_form.production_id,
                sold_at=sold_production_form.sold_at,
                customer_phone_number=sold_production_form.customer_phone_number
            )

            customer = Customer(
                fullname=sold_production_form.customer_fullname,
                address=sold_production_form.customer_address,
                phone_number=sold_production_form.customer_phone_number,
            )
            CustomerModel.insert_customer_if_not_exist(customer)

            ProductionModel.change_production_status(
                production_id=sold_production_form.production_id,
                status=ProductionStatus.SOLD
            )
            return jsonify({"success": True})
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def guarantee_production(cls):
        guarantee_production_form: GuaranteeProductionForm = from_dict(GuaranteeProductionForm, request.json)

        try:
            ProductionModel.change_production_status(
                production_id=guarantee_production_form.production_id,
                status=ProductionStatus.GUARANTEEING
            )

            guarantee_history = GuaranteeHistory(
                production_id=guarantee_production_form.production_id,
                warranty_center_id=guarantee_production_form.warranty_center_id,
                receive_at=guarantee_production_form.day_sent,
                done_guarantee_at=None,
                go_back_manufacture_factory_at=None
            )
            GuaranteeHistoryModel.guarantee_production(guarantee_history)
            return jsonify({"success": True})
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def guarantee_done(cls):
        guarantee_done_form: GuaranteeDoneForm = from_dict(GuaranteeDoneForm, request.json)

        try:
            ProductionModel.change_production_status(
                production_id=guarantee_done_form.production_id,
                status=ProductionStatus.DISTRIBUTE_BACK_TO_CUSTOMER
            )

            GuaranteeHistoryModel.guarantee_done(
                production_id=guarantee_done_form.production_id,
                day_sent=guarantee_done_form.day_sent
            )

            return jsonify({"success": True})
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def warranty_send_back_factory(cls):
        warranty_send_back_factory_form = from_dict(WarrantySendBackFactoryForm, request.json)

        try:
            ProductionModel.change_production_status(
                production_id=warranty_send_back_factory_form.production_id,
                status=ProductionStatus.ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY
            )

            GuaranteeHistoryModel.send_error_production_back_factory(
                production_id=warranty_send_back_factory_form.production_id,
                go_back_factory_at=warranty_send_back_factory_form.day_sent
            )

            return jsonify({"success": True})
        except Exception as er:
            return jsonify({"error": str(er)})

    @classmethod
    def get_product_lines(cls):
        return jsonify({
            "product_lines": ProductLineModel.get_product_lines()
        })

    @classmethod
    def get_manufacture_factories(cls):
        return jsonify({
            "manufacture_factories": ManufactureFactoryModel.get_manufacture_factories()
        })

    @classmethod
    def get_distribution_agents(cls):
        return jsonify({
            "distribution_agents": DistributionAgentModel.get_distribution_agents()
        })

    @classmethod
    def get_warranty_centers(cls):
        return jsonify({
            "warranty_centers": WarrantyCenterModel.get_warranty_centers()
        })

    @classmethod
    def get_all_productions(cls, page, per_page):
        return jsonify({
            "productions": ProductionModel.get_all_productions(page, per_page)
        })

    @classmethod
    def get_all_production_lots(cls):
        manufacture_factory: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY))

        if manufacture_factory["user_type"] != UserType.MANUFACTURE_FACTORY:
            return jsonify({"error": "User isn't manufacture factory"})

        return jsonify({
            "production_lots": ProductionLotModel.get_production_lots(manufacture_factory["id"])
        })

    @classmethod
    def get_error_productions(cls, page: int, per_page: int):
        manufacture_factory: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY))

        if manufacture_factory["user_type"] != UserType.MANUFACTURE_FACTORY:
            return jsonify({"error": "User isn't manufacture factory"})

        return jsonify({
            "productions": ProductionModel.get_error_productions(manufacture_factory["id"], page, per_page)
        })

    @classmethod
    def get_return_back_productions(cls, page: int, per_page: int):
        manufacture_factory: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY))

        if manufacture_factory["user_type"] != UserType.MANUFACTURE_FACTORY:
            return jsonify({"error": "User isn't manufacture factory"})

        return jsonify({
            "productions": ProductionModel.get_return_back_productions(manufacture_factory["id"], page, per_page)
        })

    @classmethod
    def get_on_sale_productions(cls):
        distribution_agent: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY)
        )

        if distribution_agent["user_type"] != UserType.DISTRIBUTION_AGENT:
            return jsonify({"error": "User isn't distribution agent"})

        return jsonify({
            "productions": ProductionModel.get_on_sale_productions(distribution_agent["id"])
        })

    @classmethod
    def get_sold_productions(cls, page: int, per_page: int):
        distribution_agent: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY)
        )

        if distribution_agent["user_type"] != UserType.DISTRIBUTION_AGENT:
            return jsonify({"error": "User isn't distribution agent"})

        return jsonify({
            "productions": ProductionModel.get_sold_productions(distribution_agent["id"], page, per_page)
        })

    @classmethod
    def get_guaranteeing_productions(cls, page: int, per_page: int):
        warranty_center: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY)
        )

        if warranty_center["user_type"] != UserType.WARRANTY_CENTER:
            return jsonify({"error": "User isn't warranty center"})

        return jsonify({
            "productions": ProductionModel.get_guaranteeing_productions(warranty_center["id"], page, per_page)
        })

    @classmethod
    def get_guarantee_done_productions(cls, page: int, per_page: int):
        warranty_center: UserAuthData = loads(
            request.cookies.get(USER_AUTH_DATA_KEY)
        )

        if warranty_center["user_type"] != UserType.WARRANTY_CENTER:
            return jsonify({"error": "User isn't warranty center"})

        return jsonify({
            "productions": ProductionModel.get_guarantee_done_productions(warranty_center["id"], page, per_page)
        })


