from pydantic import BaseModel


class ProductForm(BaseModel):
    title: str
    wallet: str
    price: float
    image: str


class ProductEdit(BaseModel):
    id: int
    title: str
    wallet: str
    price: float
    image: str