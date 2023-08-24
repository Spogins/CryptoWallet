import datetime
from sqlalchemy import *
from src.core.db import Base


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='NEW')
    refund = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    transaction_id = Column(Integer, ForeignKey('transaction.id'))





