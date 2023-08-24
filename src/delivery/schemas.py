from pydantic import BaseModel


class OrderForm(BaseModel):
    order: str


class OrderEdit(BaseModel):
    order: str
