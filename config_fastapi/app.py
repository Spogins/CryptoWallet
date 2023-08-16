from fastapi.middleware.cors import CORSMiddleware

from config_fastapi.test import router
from config_socketio.app import socket_app
from src.core.register import RegisterContainer
from src.users.endpoints import app as user_app
from src.auth.endpoints import app as auth_app
from src.wallet.endpoints import app as wallet_app
from src.chat.endpoints import app as chat_app
from src.ibay.endpoints import app as ibay_app
from src.parser.endpoints import app as parser
from fastapi import Depends, FastAPI




# def broker():
#     return router.broker

# @router.get("/")
# async def hello_http(broker: Annotated[RabbitBroker, Depends(broker)]):
#     await broker.publish("Hello, Rabbit!", "test")
#     return "Hello, HTTP!"


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]


def create_app() -> FastAPI:
    container = RegisterContainer()
    app = FastAPI(lifespan=router.lifespan_context)
    app.container = container
    app.include_router(ibay_app, tags=["iBay"])
    app.include_router(wallet_app, tags=["Wallets"])
    app.include_router(auth_app, tags=["Auth"])
    app.include_router(user_app, tags=["User"])
    app.include_router(chat_app, tags=["Chat"])
    app.include_router(parser, tags=['Parser'])
    app.include_router(router, tags=['Propan'])
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


# @router.after_startup
# def do_smth(app: FastAPI):
#     print('do_smth')
#     return {'do_smth': 'do_smth'}
#
#
# @router.after_startup
# async def publish_smth(app: FastAPI):
#     await router.broker.publish(("Hello, Rabbit!", "publish_smth"))
#     print('publish_smth')
#     return {'publish_smth': 'publish_smth'}


# @app.get('/startup')
# async def startup():
#     print('Create DB')
#     container = RegisterContainer()
#     db = container.db_container.db()
#     await db.create_database()




