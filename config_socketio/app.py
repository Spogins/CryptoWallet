import asyncio
import socketio
from dependency_injector.wiring import inject, Provide
from config.settings import ALLOWED_HOSTS
from src.parser.containers import Container

from src.parser.services.block_parser import ParserService

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=ALLOWED_HOSTS)


chat_room_clients = set()


@sio.on("connect")
async def connect(sid, environ):
    await sio.emit('hello', {'test': 'Hello'})
    await sio.emit('test_event', {'message': 'test'}, room=sid)  # Отправляем событие "test_event" только текущему клиенту
    # asyncio.create_task(check_block(1))
    chat_room_clients.add(sid)  # Добавляем клиента в комнату
    print(f"Client {sid} connected")


@sio.on("disconnect")
async def disconnect(sid):
    chat_room_clients.discard(sid)  # Удаляем клиента из комнаты при отключении
    print(f"Client {sid} disconnected")


@sio.on('parse_block')
@inject
async def check_block(sid, parser_service: ParserService = Provide[Container.parser_service]):
    while True:
        # print('---*---')
        block = await parser_service.get_block()
        await asyncio.sleep(1)





