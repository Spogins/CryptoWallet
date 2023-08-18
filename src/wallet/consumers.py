from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitQueue
from propan import RabbitRouter
from src.celery.wallet_tasks import wallet_hash

wallet_router = RabbitRouter('wallet/')

queue_parser = RabbitQueue(name='hash')


@wallet_router.handle(queue_parser)
async def wallet_handle(data):
    result: AsyncResult = wallet_hash.apply_async(args=[data])
    # print(f"---{data}---")
