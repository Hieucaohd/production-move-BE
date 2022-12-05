from flask import request, jsonify
from src.api.auth.forms import LoginForm
from src.api.auth.models import AdminModel, ManufactureFactoryModel, DistributionAgentModel, WarrantyCenterModel, Admin, UserType
from json import dumps
from typing import TypedDict, Optional
from dacite import from_dict


USER_AUTH_DATA_KEY = "user_auth_data"


class UserAuthData(TypedDict):
    id: str
    user_type: str


class AuthController:
    @classmethod
    def login(cls):
        login_form: LoginForm = request.json
        username = login_form['username']
        name: Optional[str] = None

        user_auth_data: UserAuthData = {
            'user_type': login_form['user_type']
        }

        if login_form['user_type'] == UserType.ADMIN:
            admin = AdminModel.find_admin_by_username(username)
            user_auth_data['id'] = admin['admin_id']
            name = admin['name']
        elif login_form['user_type'] == UserType.MANUFACTURE_FACTORY:
            manufacture_factory = ManufactureFactoryModel.find_manufacture_factory_by_username(username)
            user_auth_data['id'] = manufacture_factory['manufacture_factory_id']
            name = manufacture_factory['name']
        elif login_form['user_type'] == UserType.DISTRIBUTION_AGENT:
            distribution_agent = DistributionAgentModel.find_distribution_agent_by_username(username)
            user_auth_data['id'] = distribution_agent['distribution_agent_id']
            name = distribution_agent['name']
        elif login_form['user_type'] == UserType.WARRANTY_CENTER:
            warranty_center = WarrantyCenterModel.find_warranty_center_by_username(username)
            user_auth_data['id'] = warranty_center['warranty_center_id']
            name = warranty_center['name']

        response = jsonify({
            "name": name
        })

        response.set_cookie(USER_AUTH_DATA_KEY, value=dumps(user_auth_data), httponly=True)

        return response

    @classmethod
    def logout(cls):
        response = jsonify({
            "success": True
        })

        response.delete_cookie(USER_AUTH_DATA_KEY)
        return response

