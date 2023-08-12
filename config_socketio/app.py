import asyncio
import socketio
from config.settings import ALLOWED_HOSTS
from config_celery.celery import celery
from src.parser.containers import Container
from src.parser.services.block_parser import ParserService

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=ALLOWED_HOSTS)

socket_app = socketio.ASGIApp(sio)

celery_app = celery
parse_service = Container.parser_service()

async def my_interval_task(sid):
    while True:
        print(5)
        await parsing(parse_service)
        await asyncio.sleep(10)  # Интервал в секундах
        await sio.emit('hello', {'test': 'Hello'}, room=sid)


async def parsing(parse_service: ParserService):
    result = await parse_service.get_pending_hash()
    print(result)
    pass


@sio.on("connect")
async def connect(sid, environ):
    asyncio.create_task(my_interval_task(sid))
    await sio.emit('hello', {'test': 'Hello'})
    print(f"Client {sid} connected")


