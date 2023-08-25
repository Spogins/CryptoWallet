from dependency_injector.wiring import inject, Provide
from propan import RabbitRouter
from src.delivery.services.delivery import DeliveryService
from src.delivery.containers import Container

delivery_router = RabbitRouter('delivery/')


@inject
async def delivery_service(service: DeliveryService = Provide[Container.delivery_service]):
    return service


@delivery_router.handle('create_order')
async def delivery_handle(data):
    service: DeliveryService = await delivery_service()
    await service.create_order(data)
    # print(f"delivery_router---{data}---")


@delivery_router.handle('transaction_status')
async def transaction_status(data):
    service: DeliveryService = await delivery_service()
    await service.update_order_status(data)
    # print(f"delivery_router---{data}---")


@delivery_router.handle('refund_transaction')
async def refund_transaction(data):
    service: DeliveryService = await delivery_service()
    await service.update_order_refund(data)


@delivery_router.handle('refund_status')
async def refund_status(data):
    service: DeliveryService = await delivery_service()
    await service.update_refund_status(data)