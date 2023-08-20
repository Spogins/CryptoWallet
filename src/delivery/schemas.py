from pydantic import BaseModel


class OrderForm(BaseModel):
    order: str

