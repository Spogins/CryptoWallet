import re
from pydantic import BaseModel, ValidationError
from email_validator import validate_email, EmailNotValidError


class UserForm(BaseModel):
    id: int
    email: str
    username: str
    avatar: str


class AuthUsers(BaseModel):
    email: str
    password: str
    remember: bool = False


class RegisterUserModel(BaseModel):
    email: str
    username: str
    password: str
    confirm_password: str



