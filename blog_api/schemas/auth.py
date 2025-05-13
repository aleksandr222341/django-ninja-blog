from ninja import Schema
from typing import Optional

class UserSchema(Schema):
    id: int
    username: str
    first_name: Optional[str]


class UserLoginSchema(Schema):
    username: str
    password: str


class UserRegistrationSchema(Schema):
    first_name: str
    username: str
    email: str
    password1: str
    password2: str
    