import asyncio
import socketio


sio = socketio.AsyncClient()


@sio.on('message')
async def message(data):
    print(data)


@sio.on('balance')
async def message(data):
    print(data)


async def main():
    await sio.connect("http://localhost:8001")
    await sio.emit("parse_block")
    await sio.emit("delivery")
    await sio.wait()


if __name__ == '__main__':

    asyncio.run(main())

