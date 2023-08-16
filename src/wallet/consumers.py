from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from propan import RabbitRouter



parser_router = RabbitRouter(prefix='parser/')

queue_parser = RabbitQueue(name='hash')



@parser_router.handle(queue_parser)
async def send_hash(_hash):
    print(f'---*---{_hash}---*---')
    # result: AsyncResult = parsing.apply_async(args=[_hash])
    # # print(result)
    # # print(f"---{block}---")