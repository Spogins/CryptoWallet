# import pickle
#
# from celery.result import AsyncResult
# from propan.brokers.rabbit import RabbitQueue, RabbitExchange, ExchangeType
# from propan import RabbitRouter
# from src.celery.wallet_tasks import wallet_hash
# from utils.base.decode_data import decode_data
#
# delivery_router = RabbitRouter('delivery/')
#
# queue_parser = RabbitQueue(name='delivery')
#
# # rabbit_exchange = RabbitExchange(name='delivery', type=ExchangeType.FANOUT)
#
# @delivery_router.handle(queue_parser)
# async def delivery_handle(data):
#     print(f"delivery_router---{data}---")
