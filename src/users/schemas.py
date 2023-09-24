import re
from typing import Optional

from pydantic import (
    BaseModel,
)
from email_validator import validate_email, EmailNotValidError


class UserModel(BaseModel):
    email: str
    username: str
    password: str


class RegisterUserModel(BaseModel):
    email: str
    username: str
    password: str
    confirm_password: str


class UserProfile(BaseModel):
    username: Optional[str] = ''
    new_password: Optional[str] = ''
    repeat_password: Optional[str] = ''
    avatar: Optional[str] = ''



class UserForm(BaseModel):
    id: int
    email: str
    username: str
    avatar: str

