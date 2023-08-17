from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from propan import RabbitRouter

wallet_router = RabbitRouter('wallet/')

queue_parser = RabbitQueue(name='hash')


@wallet_router.handle(queue_parser)
async def wallet_handle(data):
    if data.get('create'):
        print('create ', data.get('create'))

    if data.get('update'):
        print('update ', data.get('update'))

    # print(f"---{data}---")
    # print(f'---*---{data}---*---')
    # result: AsyncResult = parsing.apply_async(args=[_hash])
    # # print(result)
    # # print(f"---{block}---")