from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.delivery.schemas import OrderEdit
from src.delivery.services.delivery import DeliveryService
from src.delivery.containers import Container
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


# bearer: HTTPAuthorizationCredentials = Depends(user_auth)

@app.get('/test', status_code=status.HTTP_200_OK)
@inject
async def test(delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):

    return await delivery_service.close_or_refund()


@app.get('/get_orders', status_code=status.HTTP_200_OK)
@inject
async def get_orders(delivery_service: DeliveryService = Depends(Provide[Container.delivery_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await delivery_service.get_orders(user_id)


@app.get('/get_order', status_code=status.HTTP_200_OK)
@inject
async def get_order(product: int, delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.get_order(product)


@app.put('/update_order', status_code=status.HTTP_200_OK)
@inject
async def update_order(order: OrderEdit, delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.update_order(order)
