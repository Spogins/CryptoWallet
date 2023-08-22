import socketio
from dependency_injector.wiring import inject, Provide
from socketio import AsyncAioPikaManager, AsyncServer
from config.settings import ALLOWED_HOSTS, RABBITMQ_URL
from src.web3.containers import Container
from src.web3.w3_service import WebService


mgr: AsyncAioPikaManager = socketio.AsyncAioPikaManager(RABBITMQ_URL)
sio: AsyncServer = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=ALLOWED_HOSTS, client_manager=mgr)
socket_app = socketio.ASGIApp(sio)


room_clients = set()


@sio.on("connect")
async def connect(sid, environ):
    # asyncio.create_task(check_block(1))
    room_clients.add(sid)  # Добавляем клиента в комнату
    print(f"Client {sid} connected")


@sio.on("disconnect")
async def disconnect(sid):
    room_clients.discard(sid)  # Удаляем клиента из комнаты при отключении
    print(f"Client {sid} disconnected")


@sio.on('parse_block')
@inject
async def check_block(sid, web3_service: WebService = Provide[Container.web3_service]):
    while True:
        block = await web3_service.find_block()
        # await asyncio.sleep(1)


@sio.on('join_room')
async def join_room(sid, data):
    room_name = data['room_name']
    sio.enter_room(sid, room_name)
    print(f"Client {sid} joined room {room_name}")


@sio.on('chat_room')
async def chat_room(sid, data):
    room_name = data['room_name']
    sio.enter_room(sid, room_name)
    print(f"Client {sid} joined room {room_name}")


@sio.on('leave')
async def join_room(sid, data):
    room_name = data['room_name']
    sio.leave_room(sid, room_name)
    print(f"Client {sid} leave room {room_name}")







