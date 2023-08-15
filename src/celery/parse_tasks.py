import asyncio
from asyncio import sleep

from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger

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
def parsing():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_service.get_block())
    return "Async task completed"



