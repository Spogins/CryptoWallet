import re
from typing import Optional

from pydantic import (
    BaseModel,
    FieldValidationInfo,
    ValidationError,
    field_validator,
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


    @field_validator('email')
    @classmethod
    def email_validator(cls, email: str) -> str:
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
            return email
        except EmailNotValidError as e:
            raise e


    @field_validator('password')
    @classmethod
    def email_validator(cls, password: str) -> str:
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        if re.match(pattern, password) is None:
            raise ValueError('Your password must be at least 8 characters long, be of mixed case and also contain a digit.')
        else:
            return password


    @field_validator('confirm_password')
    @classmethod
    def psw_validator(cls, confirm_password: str, values: FieldValidationInfo) -> str:
        data = values.data

        if confirm_password == data.get('password'):
            return confirm_password
        else:
            raise ValueError('password mismatch.')


class UserProfile(BaseModel):
    username: Optional[str] = ''
    new_password: Optional[str] = ''
    repeat_password: Optional[str] = ''
    avatar: Optional[str] = ''

    @field_validator('repeat_password')
    @classmethod
    def psw_validator(cls, repeat_password: str, values: FieldValidationInfo) -> str:
        data = values.data
        new_password = data.get('new_password')
        if new_password == '' and repeat_password == '':
            return ''

        if not new_password == repeat_password:
            raise ValueError('password mismatch.')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        if re.match(pattern, new_password) is None:
            raise ValueError('Your password must be at least 8 characters long, be of mixed case and also contain a digit.')
        else:
            return new_password



class UserForm(BaseModel):
    id: int
    email: str
    username: str
    avatar: str

