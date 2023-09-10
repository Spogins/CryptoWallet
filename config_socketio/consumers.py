from celery.result import AsyncResult
from dependency_injector.wiring import inject, Provide
from propan import RabbitRouter

from config_socketio.app import sio
from src.celery.wallet_tasks import wallet_hash
from src.wallet.containers import Container
from src.wallet.services.wallet import WalletService

socketio_router = RabbitRouter('socketio/')


@socketio_router.handle('send_notification')
async def send_notification(data):
    await sio.emit(event='transaction_info', data=data, room=data.get('room'))




