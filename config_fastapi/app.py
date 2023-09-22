from fastapi.middleware.cors import CORSMiddleware
from propan import RabbitBroker
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from admin.auth import AuthenticationAdmin
from config.settings import RABBITMQ_URL
from config_socketio.app import sio, check_block, delivery
from config_socketio.consumers import socketio_router
from config_socketio.socket_app import socket_app
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.chat.models import ChatMessageAdmin
from src.core.register import RegisterContainer
from src.core.routers import router_app
from src.delivery.consumers import delivery_router
from src.delivery.models import OrderAdmin
from src.ibay.models import ProductAdmin
from src.parser.consumers import parser_router
from src.users.models import UserAdmin
from src.wallet.consumers import wallet_router
from fastapi import FastAPI

from src.wallet.models import WalletAdmin, AssetAdmin, BlockchainAdmin, TransactionAdmin

broker = RabbitBroker(RABBITMQ_URL)


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001"
]

def create_app() -> FastAPI:
    container = RegisterContainer()
    app = FastAPI()
    app.container = container
    app.include_router(router_app)
    # app.include_router(router, tags=['Propan'])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/socket.io", socket_app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/admin/statics", StaticFiles(directory="admin/statics"), name="admin:statics")
    return app


app = create_app()
admin = Admin(app, RegisterContainer().db_container.db().engine, templates_dir='/admin/templates', authentication_backend=AuthenticationAdmin('admin'))
admin.add_view(UserAdmin)
admin.add_view(ChatMessageAdmin)
admin.add_view(OrderAdmin)
admin.add_view(ProductAdmin)
admin.add_view(WalletAdmin)
admin.add_view(AssetAdmin)
admin.add_view(BlockchainAdmin)
admin.add_view(TransactionAdmin)

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








