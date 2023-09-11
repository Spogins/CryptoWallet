from fastapi.middleware.cors import CORSMiddleware
from propan import RabbitBroker
from starlette.staticfiles import StaticFiles
from config_socketio.app import sio, check_block, delivery
from config_socketio.consumers import socketio_router
from config_socketio.socket_app import socket_app
from src.core.register import RegisterContainer
from src.core.routers import router_app
from src.delivery.consumers import delivery_router
from src.parser.consumers import parser_router
from src.wallet.consumers import wallet_router
from fastapi import FastAPI

broker = RabbitBroker("amqp://guest:guest@localhost:5672")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]


def create_app() -> FastAPI:
    container = RegisterContainer()
    app = FastAPI()
    app.container = container
    app.include_router(router_app)
    # app.include_router(router, tags=['Propan'])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/socket.io", socket_app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


app = create_app()


@app.on_event('startup')
async def publish_smtp():
    app.broker = broker
    app.broker.include_router(parser_router)
    app.broker.include_router(wallet_router)
    app.broker.include_router(delivery_router)
    app.broker.include_router(socketio_router)
    # sio.start_background_task(check_block)
    # sio.start_background_task(delivery)
    await broker.start()


@app.on_event('shutdown')
async def publish_smtp():
    await broker.close()








