import asyncio
import socketio
from dependency_injector.wiring import inject, Provide
from socketio import AsyncAioPikaManager, AsyncServer
from config.settings import ALLOWED_HOSTS, RABBITMQ_URL
from src.web3.containers import Container as WebContainer
from src.web3.w3_service import WebService
from src.delivery.containers import Container as DeliveryContainer
from src.delivery.services.delivery import DeliveryService

import redis.asyncio as redis

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Function to add a user to a room in Redis
async def add_user_to_room(room, username):
    await redis_client.sadd(f'room:{room}:users', username)

# Function to remove a user from a room in Redis
async def remove_user_from_room(room, username):
    await redis_client.srem(f'room:{room}:users', username)

# Function to get the list of users in a room from Redis
async def get_users_in_room(room):
    return await redis_client.smembers(f'room:{room}:users')


mgr: AsyncAioPikaManager = socketio.AsyncAioPikaManager(RABBITMQ_URL)
sio: AsyncServer = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=ALLOWED_HOSTS, client_manager=mgr)


room_clients = set()

# Создаем список активных пользователей и комнат чата
active_users = {}
# chat_rooms = {}
# room_users = {}


# Функция для отправки сообщения всем участникам комнаты
async def send_message(room, message):
    await sio.emit('message', message, room=room)


async def joined_chat(room, message):
    await sio.emit('message', message, room=room)


# Обработчик подключения клиента к серверу
@sio.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')

# Обработчик отключения клиента от сервера
@sio.event
async def disconnect(sid):
    if sid in active_users:
        user = active_users[sid]
        room = user['room']
        username = user['username']
        del active_users[sid]

        # # Удалите пользователя из списка пользователей комнаты
        # if room in room_users and username in room_users[room]:
        #     room_users[room].remove(username)
        await remove_user_from_room(room, username)
        print(username)


        await sio.emit('disconnect_user', {'room': room, 'user': username}, room=room)
        sio.leave_room(sid, room)
        # await send_message(room, f'{username} покинул чат.')


# Обработчик входа пользователя в комнату чата
@sio.on('join')
async def join_room(sid, data):
    username = data['username']
    room = data['room']
    active_users[sid] = {'username': username, 'room': room}
    sio.enter_room(sid, room)

    # Add the user to the room in Redis
    await add_user_to_room(room, username)

    # Get the list of users in the room from Redis
    room_user_list = await get_users_in_room(room)


    # Emit the updated list of users to all participants
    await sio.emit('joined_user', {'room': room, 'users': list(room_user_list)}, room=room)


    # # Добавьте пользователя в список пользователей комнаты
    # if room not in room_users:
    #     room_users[room] = []
    # room_users[room].append(username)
    #
    # # Отправьте обновленный список пользователей комнаты всем участникам
    # await sio.emit('joined_user', {'room': room, 'users': room_users[room]}, room=room)

    # await send_message(room, f'{username} присоединился к чату.')


@sio.on('send_message')
async def send_message(sid, data):
    await sio.emit('new_message', data)

# @sio.on("connect")
# async def connect(sid, environ):
#     # asyncio.create_task(check_block(1))
#     room_clients.add(sid)  # Добавляем клиента в комнату
#     print(f"Client {sid} connected")

#
# @sio.on("disconnect")
# async def disconnect(sid):
#     # room_clients.discard(sid)  # Удаляем клиента из комнаты при отключении
#     print(f"Client {sid} disconnected")


@sio.on('parse_block')
@inject
async def check_block(sid, web3_service: WebService = Provide[WebContainer.web3_service]):
    while True:
        await web3_service.find_block()
        await asyncio.sleep(1)

@sio.on('delivery')
@inject
async def delivery(sid, delivery_service: DeliveryService = Provide[DeliveryContainer.delivery_service]):
    while True:
        await asyncio.sleep(5)
        await delivery_service.close_or_refund()


# @sio.on('join')
# async def join(sid, data):
#     room = data['room']
#     sio.enter_room(sid, room)
#     await sio.emit('message', {'username': 'User', 'message': f'You joined the room "{room}".'}, room=sid)


# @sio.on('leave')
# async def join_room(sid, data):
#     room_name = data['room_name']
#     sio.leave_room(sid, room_name)
#     print(f"Client {sid} leave room {room_name}")


async def test():
    while True:
        print('*'*20)
        await asyncio.sleep(1)


