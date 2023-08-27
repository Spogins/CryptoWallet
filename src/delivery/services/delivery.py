import random
from propan import RabbitBroker
from config.settings import RABBITMQ_URL
from config_socketio.google_requests import fetch
from src.delivery.models import Order
from src.delivery.repository import DeliveryRepository


class DeliveryService:
    def __init__(self, delivery_repository: DeliveryRepository) -> None:
        self._repository: DeliveryRepository = delivery_repository

    async def close_or_refund(self):
        order: Order = await self._repository.get_oldest()
        if order:
            _random = random.randint(0, 1)
            if _random:
                await self._repository.update_order_status("SUCCESS", order.transaction_id)
                return "SUCCESS"
            else:
                await self.refund_transaction(order.transaction_id)
                return "REFUND"


    async def update_order_refund(self, data):
        await self._repository.update_order_refund(data)


    async def update_refund_status(self, data):
        status = data.get('status')
        _hash = data.get('hash')
        await self._repository.update_refund_status(status, _hash)

    async def update_order_status(self, data):

        status = data.get('status')
        trans_id = data.get('transaction_id')

        if status == "SUCCESS":
            status = "DELIVERY"
            result = await fetch()
            if not result:
                status = "FAILURE"
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

    async def get_orders(self, user_id):
        return await self._repository.get_orders(user_id)


    async def update_order(self, data):
        return await self._repository.update_order(data)
