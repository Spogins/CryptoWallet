import asyncio
from dependency_injector.wiring import Provide, inject
from config_celery.celery import celery
from src.wallet.containers import Container
from src.wallet.services.wallet import WalletService


@celery.task
@inject
def wallet_hash(_hash, wallet_service: WalletService = Provide[Container.wallet_service]):
    loop = asyncio.get_event_loop()
    if _hash.get('create'):
        print('create', _hash.get('create'))
        loop.run_until_complete(wallet_service.add_transaction(_hash.get('create')))

    elif _hash.get('update'):
        print('update', _hash.get('update'))
        loop.run_until_complete(wallet_service.transaction_update(_hash.get('update')))
    return "Async task completed"
