import asyncio
import socketio


sio = socketio.AsyncClient()

@sio.on("hello")
async def hello_handler(data):
    print(f"Received 'hello' event: {data}")


@sio.on("test_event")
async def test_event_handler(data):
    print(f"Received 'test_event' event: {data}")


@sio.on("new_message")
async def new_message_handler(data):
    print(f"Received 'new_message' event: {data}")


async def main():
    await sio.connect("http://localhost:8001")
    await sio.emit("parse_block")
    # await sio.emit("join_room", {"room": "parse_block"})
    # print("Connected and joined the room")
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())

