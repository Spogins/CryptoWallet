
from celery.result import AsyncResult
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from propan import RabbitRouter
from src.parser.containers import Container
from src.celery.parse_tasks import parsing


parser_router = RabbitRouter(prefix='parser/')

queue_parser = RabbitQueue(name='parser_queue')
parse_service = Container.parser_service()


@parser_router.handle(queue_parser)
async def send_block_in_celery(block):
    result: AsyncResult = parsing.apply_async(args=[block])

    # print(result)
    # print(f"---{block}---")

