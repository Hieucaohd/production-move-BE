from autotech_sdk.database.mongo.base_model import BaseMongoDB
from pymongo import IndexModel, ASCENDING
from typing import TypedDict
import typing
from datetime import datetime

from src.api.admin.aggregate import ProductionAggregateFactory, ProductionLotAggregateFactory


class ProductLineConfiguration(TypedDict):
    ram: str
    screen: str
    cpu: str
    camera: str
    pin: str


class ProductLine(TypedDict):
    product_line_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    configuration: ProductLineConfiguration
    price: float
    time_guarantee: str


class ProductLineModel(BaseMongoDB):
    indexes: typing.Sequence[IndexModel] = [
        IndexModel(keys=[("product_line_id", ASCENDING)],
                   unique=True, background=True)
    ]

    @classmethod
    def create_product_line(cls, product_line: ProductLine):
        inserted_id = cls.conn_primary.insert_one(product_line).inserted_id
        return bool(inserted_id)

    @classmethod
    def get_product_lines(cls) -> typing.List[ProductLine]:
        product_lines = cls.conn_secondary.find(projection={"_id": False})
        product_lines = list(product_lines)
        for product_line in product_lines:
            product_line["production_number"] = 5000
            product_line["productions_sold"] = 200
            product_line["guarantee_number"] = 300
        return product_lines


class ProductionLot(TypedDict):
    product_lot_id: str
    product_line_id: str
    manufacture_factory_id: str
    production_time: str
    production_number: int
    distribution_agent_id: str
    export_time: str


class ProductionLotModel(BaseMongoDB):
    indexes: typing.Sequence[IndexModel] = [
        IndexModel(keys=[("product_lot_id", ASCENDING)],
                   unique=True, background=True)
    ]

    @classmethod
    def create_production_lot(cls, production_lot: ProductionLot):
        inserted_id = cls.conn_primary.insert_one(production_lot).inserted_id
        return bool(inserted_id)

    @classmethod
    def export_production_lot(cls, product_lot_id: str, distribution_agent_id: str, export_time: str):
        cls.conn_primary.update_one({"product_lot_id":  product_lot_id}, {"$set": {
                                    "distribution_agent_id": distribution_agent_id, "export_time": export_time}})

    @classmethod
    def get_production_lots(cls, manufacture_factory_id: str):
        production_lots = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "manufacture_factory_id": manufacture_factory_id
                    }
                },
                *ProductionLotAggregateFactory.construct_production_lot(),
                *ProductionLotAggregateFactory.join_product_line(),
                *ProductionLotAggregateFactory.join_distribution_agent(),
                {
                    "$project": {
                        "product_lot_id": "$production_lot.product_lot_id",
                        "production_number": "$production_lot.production_number",
                        "production_time": "$production_lot.production_time",
                        "distribution_agent_name": "$distribution_agent.name",
                        "product_line": "$product_line",
                    }
                }
            ]
        )
        production_lots = list(production_lots)
        return production_lots


class ProductionStatus:
    NEW_PRODUCTION = "NEW_PRODUCTION"
    GO_TO_DISTRIBUTION = "GO_TO_DISTRIBUTION"
    SOLD = "SOLD"
    GUARANTEEING = "GUARANTEEING"
    DISTRIBUTE_BACK_TO_CUSTOMER = "DISTRIBUTE_BACK_TO_CUSTOMER"
    ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY = "ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY"
    GUARANTEE_EXPIRED = "GUARANTEE_EXPIRED"
    BACK_TO_FACTORY = "BACK_TO_FACTORY"


class Production(TypedDict):
    production_id: str
    product_lot_id: str
    status: str


class ProductionModel(BaseMongoDB):
    indexes: typing.Sequence[IndexModel] = [
        IndexModel(keys=[("production_id", ASCENDING)],
                   unique=True, background=True),
        IndexModel(keys=[("status", ASCENDING)], background=True)
    ]

    @classmethod
    def create_many_productions(cls, productions: typing.Sequence[Production]):
        inserted_ids = cls.conn_primary.insert_many(productions).inserted_ids
        return len(inserted_ids) == len(productions)

    @classmethod
    def change_many_productions_status(cls, query: dict, status: str):
        cls.conn_primary.update_many(query, {"$set": {"status": status}})

    @classmethod
    def change_production_status(cls, production_id: str, status: str):
        cls.conn_primary.update_one(
            {"production_id": production_id}, {"$set": {"status": status}})

    @classmethod
    def find_productions_by_product_lot_id(cls, product_lot_id: str) -> typing.List[Production]:
        productions = cls.conn_secondary.find({"product_lot_id": product_lot_id}, projection={"_id": False})
        return list(productions)

    @classmethod
    def get_all_productions(cls, page: int, per_page: int) -> typing.List:
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$limit": per_page*page
                },
                {
                    "$skip": per_page*(page - 1)
                },
                *ProductionAggregateFactory.query_all_production_infor(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "status": "$production.status",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "manufacture_factory_name": "$manufacture_factory.name",
                        "production_time": "$production_lot.production_time",
                        "sold_at": "$distribution_agent_warehouse.sold_at",
                        "distribution_agent_name": "$distribution_agent.name",
                        "warranty_center_name": "$warranty_center.name",
                        "customer_name": "$customer.fullname"
                    }
                },
                {
                    "$addFields": {
                        "guarantee_number": 1,  # TODO: ?????m s??? l???n b???o h??nh
                    }
                },
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_error_productions(cls, manufacture_factory_id: str, page: int, per_page: int) -> typing.List:
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "status": ProductionStatus.ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_production_lot(),
                {
                    "$match": {
                        "production_lot.manufacture_factory_id": manufacture_factory_id
                    }
                },
                {
                    "$limit": page * per_page
                },
                {
                    "$skip": per_page * (page - 1)
                },
                *ProductionAggregateFactory.join_product_line(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                *ProductionAggregateFactory.join_customer(),
                *ProductionAggregateFactory.join_distribution_agent(),
                *ProductionAggregateFactory.join_guarantee_history(),
                *ProductionAggregateFactory.join_warranty_center(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "production_time": "$production_lot.production_time",
                        "sold_at": "$distribution_agent_warehouse.sold_at",
                        "distribution_agent_name": "$distribution_agent.name",
                        "warranty_center_name": "$warranty_center.name",
                        "customer_name": "$customer.fullname"
                    }
                },
                {
                    "$addFields": {
                        "guarantee_number": 1,  # TODO: ?????m s??? l???n b???o h??nh
                    }
                },
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_return_back_productions(cls, manufacture_factory_id: str, page: int, per_page: int) -> typing.List:
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "status": ProductionStatus.BACK_TO_FACTORY
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_production_lot(),
                {
                    "$match": {
                        "production_lot.manufacture_factory_id": manufacture_factory_id
                    }
                },
                {
                    "$limit": page * per_page
                },
                {
                    "$skip": per_page * (page - 1)
                },
                *ProductionAggregateFactory.join_product_line(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                *ProductionAggregateFactory.join_distribution_agent(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "production_time": "$production_lot.production_time",
                        "distribution_agent_name": "$distribution_agent.name",
                    }
                }
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_on_sale_productions(cls, distribution_agent_id: str):
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "status": ProductionStatus.GO_TO_DISTRIBUTION
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                {
                    "$match": {
                        "distribution_agent_warehouse.distribution_agent_id": distribution_agent_id
                    }
                },
                *ProductionAggregateFactory.join_production_lot(),
                *ProductionAggregateFactory.join_manufacture_factory(),
                *ProductionAggregateFactory.join_product_line(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "manufacture_factory_name": "$manufacture_factory.name",
                        "product_line_name": "$product_line.name",
                        "ram": "$product_line.configuration.ram",
                        "screen": "$product_line.configuration.screen",
                        "cpu": "$product_line.configuration.cpu",
                        "camera": "$product_line.configuration.camera",
                        "pin": "$product_line.configuration.pin",
                        "price": "$product_line.price",
                        "production_time": "$production_lot.production_time",
                        "import_time": "$production_lot.export_time"
                    }
                }
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_sold_productions(cls, distribution_agent_id: str, page: int, per_page: int):
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "$or": [
                            {"status": {"$eq": ProductionStatus.SOLD}},
                            {"status": {"$eq": ProductionStatus.GUARANTEEING}},
                            {"status": {"$eq": ProductionStatus.DISTRIBUTE_BACK_TO_CUSTOMER}},
                            {"status": {"$eq": ProductionStatus.ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY}},
                        ]
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                {
                    "$match": {
                        "distribution_agent_warehouse.distribution_agent_id": distribution_agent_id
                    }
                },
                {
                    "$limit": per_page*page
                },
                {
                    "$skip": per_page*(page - 1)
                },
                *ProductionAggregateFactory.join_production_lot(),
                *ProductionAggregateFactory.join_manufacture_factory(),
                *ProductionAggregateFactory.join_product_line(),
                *ProductionAggregateFactory.join_guarantee_history(),
                *ProductionAggregateFactory.join_warranty_center(),
                *ProductionAggregateFactory.join_customer(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "manufacture_factory_name": "$manufacture_factory.name",
                        "production_time": "$production_lot.production_time",
                        "status": "$production.status",
                        "sold_at": "$distribution_agent_warehouse.sold_at",
                        "warranty_center_name": "$warranty_center.name",
                        "customer_name": "$customer.fullname",
                        "customer_address": "$customer.address",
                        "customer_phone_number": "$customer.phone_number"
                    }
                }
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_guaranteeing_productions(cls, warranty_center_id: str, page: int, per_page: int):
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "status": ProductionStatus.GUARANTEEING
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_guarantee_history(),
                {
                    "$match": {
                        "guarantee_history.warranty_center_id": warranty_center_id,
                    }
                },
                {
                    "$limit": per_page * page
                },
                {
                    "$skip": per_page * (page - 1)
                },
                *ProductionAggregateFactory.join_production_lot(),
                *ProductionAggregateFactory.join_product_line(),
                *ProductionAggregateFactory.join_manufacture_factory(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                *ProductionAggregateFactory.join_distribution_agent(),
                *ProductionAggregateFactory.join_customer(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "manufacture_factory_name": "$manufacture_factory.name",
                        "production_time": "$production_lot.production_time",
                        "receive_at": "$guarantee_history.receive_at",
                        "distribution_agent_name": "$distribution_agent.name",
                        "customer_name": "$customer.fullname",
                        "customer_address": "$customer.address",
                        "customer_phone_number": "$customer.phone_number"
                    }
                }
            ]
        )
        productions = list(productions)
        return productions

    @classmethod
    def get_guarantee_done_productions(cls, warranty_center_id: str, page: int, per_page: int):
        productions = cls.conn_secondary.aggregate(
            [
                {
                    "$match": {
                        "$or": [
                            {"status": {"$eq": ProductionStatus.DISTRIBUTE_BACK_TO_CUSTOMER}},
                            {"status": {"$eq": ProductionStatus.ERROR_NEED_BACK_TO_MANUFACTURE_FACTORY}},
                            {"status": {"$eq": ProductionStatus.GUARANTEE_EXPIRED}},
                        ]
                    }
                },
                *ProductionAggregateFactory.construct_production(),
                *ProductionAggregateFactory.join_guarantee_history(),
                {
                    "$match": {
                        "guarantee_history.warranty_center_id": warranty_center_id,
                    }
                },
                {
                    "$limit": per_page * page
                },
                {
                    "$skip": per_page * (page - 1)
                },
                *ProductionAggregateFactory.join_production_lot(),
                *ProductionAggregateFactory.join_product_line(),
                *ProductionAggregateFactory.join_manufacture_factory(),
                *ProductionAggregateFactory.join_distribution_agent_warehouse(),
                *ProductionAggregateFactory.join_distribution_agent(),
                *ProductionAggregateFactory.join_customer(),
                {
                    "$project": {
                        "production_id": "$production.production_id",
                        "product_line_name": "$product_line.name",
                        "product_lot_id": "$production_lot.product_lot_id",
                        "manufacture_factory_name": "$manufacture_factory.name",
                        "production_time": "$production_lot.production_time",
                        "receive_at": "$guarantee_history.receive_at",
                        "done_guarantee_at": "$guarantee_history.done_guarantee_at",
                        "status": "$production.status",
                        "distribution_agent_name": "$distribution_agent.name",
                        "customer_name": "$customer.fullname",
                        "customer_address": "$customer.address",
                        "customer_phone_number": "$customer.phone_number"
                    }
                }
            ]
        )
        productions = list(productions)
        return productions


class DistributionAgentWarehouseItem(TypedDict):
    production_id: str
    distribution_agent_id: str
    sold_at: typing.Optional[str]
    customer_phone_number: typing.Optional[str]


class DistributionAgentWarehouseModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("production_id", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def insert_many_warehouse_items(cls, warehouse_items: typing.List[DistributionAgentWarehouseItem]):
        inserted_ids = cls.conn_primary.insert_many(warehouse_items).inserted_ids
        return len(inserted_ids) == len(warehouse_items)

    @classmethod
    def import_production_lot(cls, product_lot_id: str, distribution_agent_id: str):
        productions = ProductionModel.find_productions_by_product_lot_id(product_lot_id)

        warehouse_items: typing.List[DistributionAgentWarehouseItem] = []
        for production in productions:
            warehouse_item: DistributionAgentWarehouseItem = {
                "production_id": production['production_id'],
                "distribution_agent_id": distribution_agent_id,
                "sold_at": None,
                "customer_phone_number": None
            }
            warehouse_items.append(warehouse_item)
        cls.insert_many_warehouse_items(warehouse_items)

    @classmethod
    def sold_production(cls, production_id: str, customer_phone_number: str, sold_at: str):
        cls.conn_primary.update_one({"production_id": production_id}, {"$set": {
            "customer_phone_number": customer_phone_number,
            "sold_at": sold_at
        }})


class Customer(TypedDict):
    fullname: str
    address: str
    phone_number: str


class CustomerModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("phone_number", ASCENDING)], unique=True, background=True),
    ]

    @classmethod
    def insert_customer_if_not_exist(cls, customer: Customer):
        customer_find = cls.conn_secondary.find_one({"phone_number": customer['phone_number']})
        if not customer_find:
            cls.conn_primary.insert_one(customer)


class GuaranteeHistory(TypedDict):
    warranty_center_id: str
    production_id: str
    receive_at: str
    done_guarantee_at: typing.Optional[str]
    go_back_manufacture_factory_at: typing.Optional[str]


class GuaranteeHistoryModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("production_id", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def guarantee_production(cls, guarantee_history: GuaranteeHistory):
        cls.conn_primary.insert_one(guarantee_history)

    @classmethod
    def guarantee_done(cls, production_id: str, day_sent: str):
        cls.conn_primary.update_one({"production_id": production_id}, {
            "$set": {"done_guarantee_at": day_sent}
        })

    @classmethod
    def send_error_production_back_factory(cls, production_id: str, go_back_factory_at: str):
        cls.conn_primary.update_one({"production_id": production_id},
                                    {"$set": {"go_back_manufacture_factory_at": go_back_factory_at}})


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    from autotech_sdk.database.mongo import MongoDBInit, MongoConfig
    import os
    from pprint import pprint

    mongo_config = MongoConfig(
        mongo_uri=os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        db_name=os.environ.get("DB_NAME", "prodDB")
    )
    MongoDBInit.init_client(mongo_config)
    # productions = ProductionModel.get_return_back_productions(
    #     manufacture_factory_id="d3e0947e719111ed94bbf42679426f61",
    #     page=1,
    #     per_page=10
    # )
    productions = ProductionModel.get_all_productions(1, 10)
    pprint(productions, indent=2)
