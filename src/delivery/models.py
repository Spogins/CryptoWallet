import datetime
from sqladmin import ModelView
from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.core.db import Base


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='NEW')

    refund_id = Column(Integer, ForeignKey('transaction.id'), nullable=True)
    refund = relationship('Transaction', foreign_keys=[refund_id])

    transaction_id = Column(Integer, ForeignKey('transaction.id'))
    transaction = relationship('Transaction', foreign_keys=[transaction_id])

    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', foreign_keys=[product_id])

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])




class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.date,
        Order.status,
        Order.refund_id,
        Order.refund,
        Order.transaction_id,
        Order.transaction,
        Order.product_id,
        Order.product,
        Order.user_id,
        Order.user
    ]



