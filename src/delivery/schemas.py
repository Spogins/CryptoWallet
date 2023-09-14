from pydantic import BaseModel


class OrderForm(BaseModel):
    id: int
    date: str
    status: str
    refund: str | None
    transaction: str
    product: str
    product_price: float
    product_image: str





class OrderEdit(BaseModel):
    order: str

