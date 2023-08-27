from typing import Optional
from pydantic import BaseModel


class ProductForm(BaseModel):
    title: str
    wallet: int
    price: float
    image: Optional[str] = ''


class ProductEdit(BaseModel):
    id: int
    title: str
    wallet: int
    price: float
    image: Optional[str] = ''


class BuyProduct(BaseModel):
    id: int
    wallet: str


class ProductsForm(BaseModel):
    id: int
    title: str
    wallet: str
    price: float
    image: str

