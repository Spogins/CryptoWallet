import asyncio
from config_celery.celery import celery
from src.parser.containers import Container

parse_service = Container.parser_service()


# celery.conf.beat_schedule = {
#     "parsing": {
#         "task": "src.celery.parse_tasks.parsing",
#         "schedule": 30.0  # Every 30 seconds, adjust as needed
#     },
# }


@celery.task
def parsing(block):
    print(block)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_service.parse_block(block))
    return "Async task completed"



