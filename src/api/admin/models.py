from autotech_sdk.database.mongo.base_model import BaseMongoDB
from pymongo import IndexModel, ASCENDING
from typing import TypedDict, Optional
import typing
from datetime import datetime


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
        cls.conn_primary.update_one({"product_lot_id":  product_lot_id}, {
                                    "distribution_agent_id": distribution_agent_id, "export_time": export_time})


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
                   unique=True, background=True)
    ]

    @classmethod
    def create_many_productions(cls, productions: typing.Sequence[Production]):
        inserted_ids = cls.conn_primary.insert_many(productions).inserted_ids
        return len(inserted_ids) == len(productions)

    @classmethod
    def change_many_productions_status(cls, query: dict, status: str):
        cls.conn_primary.update_many(query, {"status": status})

    @classmethod
    def change_production_status(cls, production_id: str, status: str):
        cls.conn_primary.update_one(
            {"production_id": production_id}, {"status": status})

    @classmethod
    def find_productions_by_product_lot_id(cls, product_lot_id: str) -> typing.List[Production]:
        productions = cls.conn_secondary.find({"product_lot_id": product_lot_id})
        return list(productions)


class DistributionAgentWarehouseItem(TypedDict):
    production_id: str
    distribution_agent_id: str
    sold_at: typing.Optional[str]
    customer_id: typing.Optional[str]


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
                "customer_id": None
            }
            warehouse_items.append(warehouse_item)
        cls.insert_many_warehouse_items(warehouse_items)

    @classmethod
    def sold_production(cls, production_id: str, customer_phone_number: str, sold_at: str):
        cls.conn_primary.update_one({"production_id": production_id}, {
            "customer_phone_number": customer_phone_number,
            "sold_at": sold_at
        })


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
        customer = cls.conn_secondary.find_one({"phone_number": customer['phone_number']})
        if not customer:
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
            "done_guarantee_at": day_sent
        })

