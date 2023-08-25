import datetime
from sqlalchemy import *
from src.core.db import Base


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='NEW')
    refund = Column(String, nullable=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    transaction = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))




