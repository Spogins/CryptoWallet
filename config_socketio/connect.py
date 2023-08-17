import asyncio

import socketio


sio = socketio.AsyncClient()

## Обработчик события "hello" (от сервера)
@sio.on("hello")
async def hello_handler(data):
    print(f"Received 'hello' event: {data}")


# Обработчик события "test_event" (от сервера)
@sio.on("test_event")
async def test_event_handler(data):
    print(f"Received 'test_event' event: {data}")


# Обработчик события "new_message" (от сервера)
@sio.on("new_message")
async def new_message_handler(data):
    print(f"Received 'new_message' event: {data}")

# Асинхронная функция для подключения и присоединения к комнате
async def main():
    await sio.connect("http://localhost:8001")
    await sio.emit("parse_block")
    # await sio.emit("join_room", {"room": "parse_block"})
    # print("Connected and joined the room")
    await sio.wait()


# # Запуск асинхронной функции
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())

if __name__ == '__main__':
    asyncio.run(main())

