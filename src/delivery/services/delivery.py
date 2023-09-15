import random
from propan import RabbitBroker
from config.settings import RABBITMQ_URL
from config_socketio.google_requests import fetch, run_delivery
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
                order = await self._repository.update_order_status("SUCCESS", order.transaction_id)
                await self.send_update_order(order)
                return "SUCCESS"
            else:
                await self.refund_transaction({'trans_id': order.transaction_id, 'status': 'REFUND'})
                await self._repository.update_order_status("REFUND", order.transaction_id)
                return "REFUND"


    async def update_order_refund(self, data):
        order = await self._repository.update_order_refund(data)
        await self.send_update_order(order)


    async def send_update_order(self,order):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            data = {
                'id': order.id,
                'status': order.status,
                'transaction': order.transaction.hash,
                'refund': order.refund.hash if order.refund else False,
                'room': order.user_id
            }
            await broker.publish(message=data, queue='socketio/update_order')

    async def update_refund_status(self, data):
        status = data.get('status')
        refund_id = data.get('refund_id')
        await self._repository.update_refund_status(status, refund_id)

    async def update_order_status(self, data):

        status = data.get('status')
        trans_id = data.get('transaction_id')

        if status == "SUCCESS":
            status = "DELIVERY"
            result = await run_delivery()
            if not result:
                status = "FAILURE"
                await self.refund_transaction({'trans_id': trans_id, 'status': status})

        if status == "FAILURE":
            status = "FAILURE"
            await self.refund_transaction({'trans_id': trans_id, 'status': status})

        order = await self._repository.update_order_status(status, trans_id)
        await self.send_update_order(order)
        return order

    @staticmethod
    async def refund_transaction(trans_id):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=trans_id, queue='wallet/refund_transaction')

    async def create_order(self, data):
        new_order = await self._repository.add(data)
        order = await self._repository.get_order(new_order.id)
        async with RabbitBroker(RABBITMQ_URL) as broker:
            data = {
                'id': order.id,
                'date': order.date,
                'status': order.status,
                'refund': order.refund,
                'transaction': order.transaction,
                'product': order.product,
                'product_price': order.product_price,
                'product_image': order.product_image,
                'room': new_order.user_id
            }
            await broker.publish(message=data, queue='socketio/new_order')


    async def get_order(self, order_id):
        return await self._repository.get_order(order_id)

    async def get_orders(self, user_id):
        return await self._repository.get_orders(user_id)


    async def update_order(self, data):
        return await self._repository.update_order(data)
