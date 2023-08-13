import asyncio
import socketio
from config.settings import ALLOWED_HOSTS
from config_celery.celery import celery
from src.parser.containers import Container
from src.parser.services.block_parser import ParserService
from sqlalchemy.orm import clear_mappers



sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=ALLOWED_HOSTS)

socket_app = socketio.ASGIApp(sio)

celery_app = celery
parse_service = Container.parser_service()

async def my_interval_task(sid):
    while True:
        await parsing(parse_service)
        await asyncio.sleep(5)  # Интервал в секундах
        await sio.emit('hello', {'test': 'Hello'}, room=sid)


async def parsing(parse_service: ParserService):
    result = await parse_service.get_pending_hash()
    print(result)

#
#
# @sio.on("connect")
# async def connect(sid, environ):
#     asyncio.create_task(my_interval_task(sid))
#     await sio.emit('hello', {'test': 'Hello'})
#     print(f"Client {sid} connected")


chat_room_clients = set()
#
# Обработчик события подключения
@sio.on("connect")
async def connect(sid, environ):
    await sio.emit('hello', {'test': 'Hello'})
    await sio.emit('test_event', {'message': 'test'}, room=sid)  # Отправляем событие "test_event" только текущему клиенту
    chat_room_clients.add(sid)  # Добавляем клиента в комнату
    print(f"Client {sid} connected")

# Обработчик события присоединения к комнате
@sio.on("join_room")
async def join_room(sid, data):
    room_name = data.get('room')
    sio.enter_room(sid, room_name)
    if room_name == 'parse_block':
        print(f'Start parsing.')
        asyncio.create_task(my_interval_task(sid))
    chat_room_clients.add(sid)  # Добавляем клиента в комнату
    print(f"Client {sid} joined room {room_name}")


# Обработчик события отправки сообщения
@sio.on("send_message")
async def send_message(sid, data):
    room_name = data.get('room')
    message = data.get('message')
    await sio.emit('new_message', {'message': message}, room=room_name)
    print(f"Client {sid} sent a message to room {room_name}")

# Обработчик события отключения
@sio.on("disconnect")
async def disconnect(sid):
    chat_room_clients.discard(sid)  # Удаляем клиента из комнаты при отключении
    print(f"Client {sid} disconnected")




