from celery.result import AsyncResult
from dependency_injector.wiring import inject, Provide
from propan import RabbitRouter
from src.celery.wallet_tasks import wallet_hash
from src.wallet.containers import Container
from src.wallet.services.wallet import WalletService

wallet_router = RabbitRouter('wallet/')


@wallet_router.handle('hash')
async def wallet_handle(data):
    result: AsyncResult = wallet_hash.apply_async(args=[data])
    # print(f"---{data}---")


@inject
async def wallet_service(service: WalletService = Provide[Container.wallet_service]):
    return service


@wallet_router.handle('buy_product')
async def buy_product(data):
    service: WalletService = await wallet_service()
    await service.buy_product(data)


@wallet_router.handle('refund_transaction')
async def buy_product(data):
    service: WalletService = await wallet_service()
    await service.refund(data)

