import typing


class AggregateFactory:
    @classmethod
    def create_project_field_map(cls, include_fields: typing.List[str], include: int = 1):
        fields_map = {}
        for field in include_fields:
            fields_map[field] = include
        return fields_map

    @classmethod
    def construct_self_field(cls, fields: typing.List[str]):
        aggregate_command = {}
        for field in fields:
            aggregate_command[field] = f"${field}"
        return aggregate_command


class ProductionAggregateFactory(AggregateFactory):
    @classmethod
    def join_production_lot(cls):
        """
        Giả định result trước đó của pipeline chứa field production
        """
        from src.api.admin.models import ProductionLotModel
        return [
            {
                "$lookup": {
                    "from": ProductionLotModel.COLLECTION_NAME,
                    "localField": "production.product_lot_id",
                    "foreignField": "product_lot_id",
                    "as": "product_lots"
                }
            },
            {
                "$addFields": {
                    "production_lot": {"$first": "$product_lots"},
                }
            },
            {
                "$unset": ["product_lots", "production_lot._id"]
            }
        ]

    @classmethod
    def join_manufacture_factory(cls):
        """
        Giả định result trước đó của pipeline chứa filed production_lot
        """
        from src.api.auth.models import ManufactureFactoryModel
        return [
            {
                "$lookup": {
                    "from": ManufactureFactoryModel.COLLECTION_NAME,
                    "localField": "production_lot.manufacture_factory_id",
                    "foreignField": "manufacture_factory_id",
                    "as": "manufacture_factories"
                }
            },
            {
                "$addFields": {
                    "manufacture_factory": {"$first": "$manufacture_factories"},
                }
            },
            {
                "$unset": ["manufacture_factories", "manufacture_factory._id"]
            }
        ]

    @classmethod
    def join_product_line(cls):
        """
        Giả định result trước đó của pipeline chứa field production_lot
        """
        from src.api.admin.models import ProductLineModel
        return [
            {
                "$lookup": {
                    "from": ProductLineModel.COLLECTION_NAME,
                    "localField": "production_lot.product_line_id",
                    "foreignField": "product_line_id",
                    "as": "product_lines"
                }
            },
            {
                "$addFields": {
                    "product_line": {"$first": "$product_lines"},
                }
            },
            {
                "$unset": ["product_lines", "product_line._id"]
            }
        ]

    @classmethod
    def join_customer(cls):
        """
        Giả định result trước đó của pipeline chứa field distribution_agent_warehouse
        """
        from src.api.admin.models import CustomerModel
        return [
            {
                "$lookup": {
                    "from": CustomerModel.COLLECTION_NAME,
                    "localField": "distribution_agent_warehouse.customer_phone_number",
                    "foreignField": "phone_number",
                    "as": "customers"
                }
            },
            {
                "$addFields": {
                    "customer": {"$first": "$customers"},
                }
            },
            {
                "$unset": ["customers", "customer._id"]
            }
        ]

    @classmethod
    def join_distribution_agent_warehouse(cls):
        """
        Giả định result trước đó của pipeline chứa field production
        """
        from src.api.admin.models import DistributionAgentWarehouseModel
        return [
            {
                "$lookup": {
                    "from": DistributionAgentWarehouseModel.COLLECTION_NAME,
                    "localField": "production.production_id",
                    "foreignField": "production_id",
                    "as": "distribution_agent_warehouses"
                }
            },
            {
                "$addFields": {
                    "distribution_agent_warehouse": {"$first": "$distribution_agent_warehouses"},
                }
            },
            {
                "$unset": ["distribution_agent_warehouses", "distribution_agent_warehouse._id"]
            },
        ]

    @classmethod
    def join_distribution_agent(cls):
        """
        Giả định result trước đó của pipeline chứa field distribution_agent_warehouse
        """
        from src.api.auth.models import DistributionAgentModel
        return [
            {
                "$lookup": {
                    "from": DistributionAgentModel.COLLECTION_NAME,
                    "localField": "distribution_agent_warehouse.distribution_agent_id",
                    "foreignField": "distribution_agent_id",
                    "as": "distribution_agents"
                }
            },
            {
                "$addFields": {
                    "distribution_agent": {"$first": "$distribution_agents"},
                }
            },
            {
                "$unset": ["distribution_agents", "distribution_agent._id"]
            }
        ]

    @classmethod
    def join_guarantee_history(cls):
        """
        Giả định result trước đó của pipeline chứa field production
        """
        from src.api.admin.models import GuaranteeHistoryModel
        return [
            {
                "$lookup": {
                    "from": GuaranteeHistoryModel.COLLECTION_NAME,
                    "localField": "production.production_id",
                    "foreignField": "production_id",
                    "as": "guarantee_histories"
                }
            },
            {
                "$addFields": {
                    "guarantee_history": {"$first": "$guarantee_histories"},
                }
            },
            {
                "$unset": ["guarantee_histories", "guarantee_history._id"]
            }
        ]

    @classmethod
    def join_warranty_center(cls):
        """
        Giả định result trước đó của pipeline chứa field guarantee_history
        """
        from src.api.auth.models import WarrantyCenterModel
        return [
            {
                "$lookup": {
                    "from": WarrantyCenterModel.COLLECTION_NAME,
                    "localField": "guarantee_history.warranty_center_id",
                    "foreignField": "warranty_center_id",
                    "as": "warranty_centers"
                }
            },
            {
                "$addFields": {
                    "warranty_center": {"$first": "$warranty_centers"},
                }
            },
            {
                "$unset": ["warranty_centers", "warranty_center._id"]
            }
        ]

    @classmethod
    def construct_production(cls):
        fields = ["production_id", "product_lot_id", "status"]
        return [
            {
                "$addFields": {
                    "production": {
                        **cls.construct_self_field(fields)
                    }
                }
            },
            {
                "$unset": ["_id", *fields]
            },
        ]

    @classmethod
    def query_all_production_infor(cls):
        return [
            *cls.construct_production(),
            *cls.join_distribution_agent_warehouse(),
            *cls.join_customer(),
            *cls.join_distribution_agent(),
            *cls.join_production_lot(),
            *cls.join_product_line(),
            *cls.join_manufacture_factory(),
            *cls.join_guarantee_history(),
            *cls.join_warranty_center()
        ]


class ProductionLotAggregateFactory(AggregateFactory):
    @classmethod
    def join_product_line(cls):
        """
        Giả định result trước đó của pipeline chứa field production_lot
        """
        return ProductionAggregateFactory.join_product_line()

    @classmethod
    def join_distribution_agent(cls):
        """
        Giả định result trước đó của pipeline chứa field production_lot
        """
        from src.api.auth.models import DistributionAgentModel
        return [
            {
                "$lookup": {
                    "from": DistributionAgentModel.COLLECTION_NAME,
                    "localField": "production_lot.distribution_agent_id",
                    "foreignField": "distribution_agent_id",
                    "as": "distribution_agents"
                }
            },
            {
                "$addFields": {
                    "distribution_agent": {"$first": "$distribution_agents"},
                }
            },
            {
                "$unset": ["distribution_agents", "distribution_agent._id"]
            }
        ]

    @classmethod
    def construct_production_lot(cls):
        fields = [
            "product_lot_id",
            "product_line_id",
            "manufacture_factory_id",
            "production_time",
            "production_number",
            "distribution_agent_id",
            "export_time",
        ]
        return [
            {
                "$addFields": {
                    "production_lot": {
                        **cls.construct_self_field(fields)
                    }
                }
            },
            {
                "$unset": ["_id", *fields]
            },
        ]
