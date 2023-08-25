from typing import Callable

from asyncpg import Record
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.delivery.models import Order


class DeliveryRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def update_refund_status(self, status, _hash):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.refund == _hash))
            order: Order = result.scalar_one_or_none()
            if order:
                order.status = status
                await session.commit()
                await session.refresh(order)

    async def update_order_refund(self, data):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.transaction == data.get('trans_hash')))
            order: Order = result.scalar_one_or_none()
            if order:
                order.refund = data.get('ref_hash')
                await session.commit()
                await session.refresh(order)

    async def get_oldest(self):
        async with self.session_factory() as session:
            oldest_record = await session.execute(select(Order).where(Order.status == "DELIVERY").order_by(Order.date))
            res = oldest_record.scalars().first()
            return res

    async def update_order_status(self, status, _hash):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.transaction == _hash))
            order: Order = result.scalar_one_or_none()
            if order:
                order.status = status
                await session.commit()
                await session.refresh(order)

    async def add(self, data):
        print(data)

        async with self.session_factory() as session:
            order: Order = Order(
                product_id=data.get('product_id'),
                transaction=data.get('transaction'),
                user_id=data.get('user_id')
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def get_order(self, order_id):
        async with self.session_factory() as session:
            order = await session.get(Order, order_id)
            if order:
                return order
            else:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {order_id}")

    async def get_orders(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.user_id == user_id))
            orders = result.scalars().all()
            return orders





