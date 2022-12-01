from typing import TypedDict


class LoginForm(TypedDict):
    username: str
    password: str
    user_type: str
