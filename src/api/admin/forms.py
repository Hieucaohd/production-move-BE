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
	price: str
	time_guarantee: str
	configuration: ProductLineConfiguration


class CreateProductionLotForm(TypedDict):
	product_line_id: str
	production_number: int
	production_time: str


class ExportProductionLotForm(TypedDict):
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
