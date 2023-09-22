from sqladmin import ModelView
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db import Base
from sqlalchemy_utils import URLType


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default='Product')
    image = Column(URLType, nullable=True)
    price = Column(DECIMAL, default=0)
    in_order = Column(Boolean, default=False)

    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    wallet = relationship('Wallet', foreign_keys=[wallet_id])

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.title,
        Product.image,
        Product.price,
        Product.in_order,
        Product.wallet_id,
        Product.wallet,
        Product.user_id,
        Product.user
    ]