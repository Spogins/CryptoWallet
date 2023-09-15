from _decimal import Decimal
from typing import Callable

from asyncpg import Record
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.delivery.models import Order
from src.delivery.schemas import OrderForm


class DeliveryRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def update_refund_status(self, status, refund_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.refund_id == refund_id))
            order: Order = result.scalar_one_or_none()
            if order:
                order.status = status
                await session.commit()
                await session.refresh(order)

    async def update_order_refund(self, data):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(joinedload(Order.refund)).where(Order.transaction_id == data.get('transaction_id')))
            order: Order = result.scalar_one_or_none()
            if order:
                order.refund_id = data.get('ref_transaction_id')
                await session.commit()
                await session.refresh(order)
                return order

    async def get_oldest(self):
        async with self.session_factory() as session:
            oldest_record = await session.execute(select(Order).where(Order.status == "DELIVERY" and Order.refund_id is None).order_by(Order.date))
            res = oldest_record.scalars().first()
            return res

    async def update_order_status(self, status, trans_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(joinedload(Order.refund)).where(Order.transaction_id == trans_id))
            order: Order = result.scalar_one_or_none()
            if order:
                order.status = status
                await session.commit()
                await session.refresh(order)
                return order

    async def add(self, data):
        async with self.session_factory() as session:
            order: Order = Order(
                product_id=data.get('product_id'),
                transaction_id=data.get('transaction_id'),
                user_id=data.get('user_id')
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def get_order(self, order_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(joinedload(Order.refund)).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if not order:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {order_id}")
            return OrderForm(
                id=order.id,
                date=str(order.date),
                status=order.status,
                refund=order.refund.hash if order.refund else None,
                transaction=order.transaction.hash,
                product=order.product.title,
                product_price=Decimal(order.product.price),
                product_image=order.product.image
            )

    async def get_orders(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(joinedload(Order.refund)).where(Order.user_id == user_id))
            orders = result.scalars().all()
            return [OrderForm(
                id=order.id,
                date=str(order.date),
                status=order.status,
                refund=order.refund.hash if order.refund else None,
                transaction=order.transaction.hash,
                product=order.product.title,
                product_price=Decimal(order.product.price),
                product_image=order.product.image
            ) for order in orders]





