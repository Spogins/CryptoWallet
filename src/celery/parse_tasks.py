import asyncio
from dependency_injector.wiring import Provide, inject
from config_celery.celery import celery
from src.parser.containers import Container
from src.parser.services.block_parser import ParserService


@celery.task
@inject
def parsing(block, parser_service: ParserService = Provide[Container.parser_service]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_service.parse_block(block))
    return "Async task completed"





