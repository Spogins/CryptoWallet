from fastapi.middleware.cors import CORSMiddleware
from propan import RabbitBroker
from config_socketio.socket_app import socket_app
from src.core.register import RegisterContainer
from src.parser.consumers import parser_router
from src.users.endpoints import app as user_app
from src.auth.endpoints import app as auth_app
from src.wallet.consumers import wallet_router
from src.wallet.endpoints import app as wallet_app
from src.chat.endpoints import app as chat_app
from src.ibay.endpoints import app as ibay_app
from src.delivery.endpoints import app as delivery_app
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

    app.include_router(ibay_app, tags=["iBay"])
    app.include_router(wallet_app, tags=["Wallets"])
    app.include_router(auth_app, tags=["Auth"])
    app.include_router(user_app, tags=["User"])
    app.include_router(chat_app, tags=["Chat"])
    app.include_router(delivery_app, tags=["Delivery"])
    # app.include_router(router, tags=['Propan'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/socket.io", socket_app)
    return app


app = create_app()


# @app.get('/test')
# @inject
# async def test():
#     return {'message': 'text'}


@app.on_event('startup')
async def publish_smtp():
    app.broker = broker
    app.broker.include_router(parser_router)
    app.broker.include_router(wallet_router)
    print('startup')
    await broker.start()


@app.on_event('shutdown')
async def publish_smtp():
    print('shut_down')
    await broker.close()





