import pickle

from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from propan import RabbitRouter
from src.celery.parse_tasks import parsing


parser_router = RabbitRouter('parser/')

queue_parser = RabbitQueue(name='parse_block')


# @parser_router.handle(queue_parser)
# async def parser(data):
#     data = pickle.loads(data)
#     print(f"parser_router---{data}---")


@parser_router.handle(queue_parser)
async def parser_handle(block):
    result: AsyncResult = parsing.apply_async(args=[block])


