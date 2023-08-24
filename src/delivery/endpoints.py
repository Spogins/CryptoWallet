from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.delivery.schemas import OrderEdit
from src.delivery.services.delivery import DeliveryService
from src.delivery.containers import Container


app = APIRouter()

user_auth = AutoModernJWTAuth()


# bearer: HTTPAuthorizationCredentials = Depends(user_auth)

@app.get('/get_orders', status_code=status.HTTP_200_OK)
@inject
async def get_orders(delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.get_orders()


@app.get('/get_order', status_code=status.HTTP_200_OK)
@inject
async def get_order(product: int, delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.get_order(product)


@app.put('/update_order', status_code=status.HTTP_200_OK)
@inject
async def update_order(order: OrderEdit, delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.update_order(order)


@app.delete('/delete_order', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_order(order: int, delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return await delivery_service.remove_order(order)
