
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter
from src.parser.containers import Container
from src.parser.services.block_parser import ParserService

app = APIRouter()


@app.put('/parse_block')
@inject
async def parse_block(parser_service: ParserService = Depends(Provide[Container.parser_service])):
    return await parser_service.get_pending_hash()



