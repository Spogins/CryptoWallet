from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.delivery.services.delivery import DeliveryService
from src.delivery.containers import Container


app = APIRouter()

user_auth = AutoModernJWTAuth()


# bearer: HTTPAuthorizationCredentials = Depends(user_auth)

@app.get("/test", status_code=status.HTTP_200_OK)
@inject
async def test(delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    return {'m': 'l'}





