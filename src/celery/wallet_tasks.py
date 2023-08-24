import asyncio
from dependency_injector.wiring import Provide, inject
from config_celery.celery import celery
from src.wallet.containers import Container
from src.wallet.services.wallet import WalletService


@celery.task
@inject
def wallet_hash(_hash, wallet_service: WalletService = Provide[Container.wallet_service]):
    loop = asyncio.get_event_loop()

    if _hash.get('hash'):
        print(f"hash: {_hash.get('hash')}")
        loop.run_until_complete(wallet_service.create_or_update(_hash.get('hash')))

    return "Async task completed"
