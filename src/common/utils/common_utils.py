from uuid import uuid1
from flask import request
from src.api.auth.controllers import USER_AUTH_DATA_KEY


def generate_uuid():
	return uuid1().hex


def get_user_auth_data():
	# data = request.cookies.get(USER_AUTH_DATA_KEY)
	data = request.headers.get(USER_AUTH_DATA_KEY)
	return data
