from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.delivery.models import Order


class DeliveryRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory


    async def update_order_status(self, status, trans_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Order).where(Order.transaction_id == trans_id))
            order: Order = result.scalar_one_or_none()
            if order:
                order.status = status
                await session.commit()
                await session.refresh(order)

    async def add(self, data):
        try:
            async with self.session_factory() as session:
                order: Order = Order(
                    product_id=data.get('product_id'),
                    transaction_id=data.get('trans_id')
                )
                session.add(order)
                await session.commit()
                await session.refresh(order)
                return order
        except:
            raise HTTPException(status_code=401,
                                detail='Wrong input data')

    async def get_order(self, order_id):
        async with self.session_factory() as session:
            order = await session.get(Order, order_id)
            if order:
                return order
            else:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {order_id}")

    async def get_orders(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Order))
            orders = result.scalars().all()
            return orders

    async def remove_order(self, order_id):
        async with self.session_factory() as session:
            order = await session.get(Order, order_id)
            if not order:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {order_id}")
            await session.delete(order_id)
            await session.commit()

    async def update_order(self, data):
        pass





