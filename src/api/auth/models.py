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
