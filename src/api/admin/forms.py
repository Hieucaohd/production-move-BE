from typing import TypedDict
from src.api.admin.models import ProductLineConfiguration
from dataclasses import dataclass


class CreateManufactureFactoryForm(TypedDict):
    username: str
    password: str
    name: str
    address: str
    phone_number: str


class CreateDistributionAgentForm(TypedDict):
    username: str
    password: str
    name: str
    address: str
    phone_number: str


class CreateWarrantyCenterForm(TypedDict):
    username: str
    password: str
    name: str
    address: str
    phone_number: str


class CreateProductLineForm(TypedDict):
    name: str
    price: float
    time_guarantee: str
    configuration: ProductLineConfiguration


@dataclass
class CreateProductionLotForm:
    product_line_id: str
    production_number: int
    production_time: str


@dataclass
class ExportProductionLotForm:
    product_lot_id: str
    distribution_agent_id: str
    export_time: str


@dataclass
class SoldProductionForm:
    production_id: str
    customer_fullname: str
    customer_address: str
    customer_phone_number: str
    sold_at: str


@dataclass
class GuaranteeProductionForm:
    production_id: str
    warranty_center_id: str
    day_sent: str


@dataclass
class GuaranteeDoneForm:
    production_id: str
    day_sent: str


@dataclass
class WarrantySendBackFactoryForm:
    production_id: str
    day_sent: str


@dataclass
class DistributionAgentSendBackFactoryForm:
    production_id: str
    day_sent: str


if __name__ == '__main__':
    create = CreateProductionLotForm(product_line_id="1", production_number=2, production_time="3")
    print(create.__dict__)
