import typing

from autotech_sdk.database.mongo.base_model import BaseMongoDB
from pymongo import IndexModel, ASCENDING
from typing import TypedDict, Optional
from datetime import datetime


class UserType:
    ADMIN = "ADMIN"
    MANUFACTURE_FACTORY = "MANUFACTURE_FACTORY"
    DISTRIBUTION_AGENT = "DISTRIBUTION_AGENT"
    WARRANTY_CENTER = "WARRANTY_CENTER"


class Admin(TypedDict):
    admin_id: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    name: str


class AdminModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("username", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def find_admin_by_username(cls, username: str):
        admin: Admin = cls.conn_secondary.find_one({"username": username})
        return admin


class ManufactureFactory(TypedDict):
    manufacture_factory_id: Optional[str]
    admin_id: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    name: str
    address: str
    phone_number: str


class ManufactureFactoryModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("username", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def find_manufacture_factory_by_username(cls, username: str):
        manufacture_factory: ManufactureFactory = cls.conn_secondary.find_one({"username": username})
        return manufacture_factory
    
    @classmethod
    def create_manufacture_factory(cls, manufacture_factory: ManufactureFactory):
        inserted_id = cls.conn_primary.insert_one(manufacture_factory)
        if inserted_id:
            return True
        return False

    @classmethod
    def get_manufacture_factories(cls) -> typing.List[ManufactureFactory]:
        manufacture_factories = cls.conn_secondary.find()
        for manufacture_factory in manufacture_factories:
            manufacture_factory["production_number"] = 1000000
            manufacture_factory["productions_distributed"] = 100
            manufacture_factory["guarantee_number"] = 50
            manufacture_factory["error_number"] = 20
            manufacture_factory["production_return_back_number"] = 2
        return list(manufacture_factories)


class DistributionAgent(TypedDict):
    distribution_agent_id: str
    admin_id: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    name: str
    address: str
    phone_number: str


class DistributionAgentModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("username", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def find_distribution_agent_by_username(cls, username: str):
        distribution_agent: DistributionAgent = cls.conn_secondary.find_one({"username": username})
        return distribution_agent
    
    @classmethod
    def create_distribution_agent(cls, distribution_agent: DistributionAgent):
        inserted_id = cls.conn_primary.insert_one(distribution_agent)
        if inserted_id:
            return True
        return False

    @classmethod
    def get_distribution_agents(cls) -> typing.List[DistributionAgent]:
        distribution_agents = cls.conn_secondary.find()
        for distribution_agent in distribution_agents:
            distribution_agent["received_productions_number"] = 1000
            distribution_agent["productions_sold"] = 100
            distribution_agent["return_back"] = 5
        return list(distribution_agents)


class WarrantyCenter(TypedDict):
    warranty_center_id: str
    admin_id: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    name: str
    address: str
    phone_number: str


class WarrantyCenterModel(BaseMongoDB):
    indexes = [
        IndexModel(keys=[("username", ASCENDING)], unique=True, background=True)
    ]

    @classmethod
    def find_warranty_center_by_username(cls, username: str):
        warranty_center: WarrantyCenter = cls.conn_secondary.find_one({"username": username})
        return warranty_center

    @classmethod
    def create_warranty_center(cls, warranty_center: WarrantyCenter):
        inserted_id = cls.conn_primary.insert_one(warranty_center)
        if inserted_id:
            return True
        return False

    @classmethod
    def get_warranty_centers(cls) -> typing.List[WarrantyCenter]:
        warranty_centers = cls.conn_secondary.find()
        for warranty_center in warranty_centers:
            warranty_center["guaranteeing_number"] = 1000
            warranty_center["guarantee_done_number"] = 100
            warranty_center["can_not_guarantee"] = 10
        return list(warranty_centers)
