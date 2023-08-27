import asyncio
from time import sleep

import socketio


sio = socketio.AsyncClient()


@sio.event
async def message(data):
    print(data)

@sio.event
def my_message(sid, data):
    sio.emit('my reply', data, room='chat_room', skip_sid=sid)



async def main():
    await sio.connect("http://localhost:8001")
    await sio.emit('join', {'room': 'chat_room'})
    sleep(5)
    await sio.emit('message', data='str')
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
