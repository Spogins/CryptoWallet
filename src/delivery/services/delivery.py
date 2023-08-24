import asyncio

from fastapi import HTTPException
from propan import RabbitBroker

from config.settings import RABBITMQ_URL
from config_socketio.google_requests import fetch
from src.delivery.repository import DeliveryRepository


class DeliveryService:
    def __init__(self, delivery_repository: DeliveryRepository) -> None:
        self._repository: DeliveryRepository = delivery_repository

    async def update_order_status(self, data):
        trans_id = data.get('trans_id')
        status = data.get('status')
        _hash = data.get('_hash')

        if status == "SUCCESS":
            # loop = asyncio.get_event_loop()
            result = await fetch()
            if not result:
                await self.refund_transaction(trans_id)

        if status == "FAILURE":
            await self.refund_transaction(trans_id)

        await self._repository.update_order_status(status, trans_id)

    @staticmethod
    async def refund_transaction(trans_id):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=trans_id, queue='wallet/refund_transaction')

    async def create_order(self, data):
        return await self._repository.add(data)

    async def get_order(self, order_id):
        return await self._repository.get_order(order_id)

    async def get_orders(self):
        return await self._repository.get_orders()

    async def remove_order(self, order_id):
        return await self._repository.remove_order(order_id)

    async def update_order(self, data):
        return await self._repository.update_order(data)
