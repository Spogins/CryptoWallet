import pickle

from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitQueue, RabbitExchange, ExchangeType
from propan import RabbitRouter
from src.celery.wallet_tasks import wallet_hash

wallet_router = RabbitRouter('wallet/')

queue_parser = RabbitQueue(name='hash')

# rabbit_exchange = RabbitExchange(name='wallet', type=ExchangeType.FANOUT)


# @wallet_router.handle('wallet', exchange=rabbit_exchange)
# async def wallet_handle(data):
#     data = pickle.loads(data)
#     print(f"delivery_router---{data}---")

@wallet_router.handle(queue_parser)
async def wallet_handle(data):
    result: AsyncResult = wallet_hash.apply_async(args=[data])
    # print(f"---{data}---")
