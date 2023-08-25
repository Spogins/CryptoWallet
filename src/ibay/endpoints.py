from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.ibay.containers import Container
from src.ibay.schemas import ProductForm, ProductEdit, BuyProduct
from src.ibay.services.ibay import IBayService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


@app.post('/add_product', status_code=status.HTTP_201_CREATED)
@inject
async def add_product(product: ProductForm, ibay_service: IBayService = Depends(Provide[Container.ibay_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await ibay_service.add_product(product, user_id)


@app.get('/get_products', status_code=status.HTTP_200_OK)
@inject
async def get_products(ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    return await ibay_service.get_products()


@app.get('/get_product', status_code=status.HTTP_200_OK)
@inject
async def get_product(product: int, ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    return await ibay_service.get_product(product)


@app.put('/update_product', status_code=status.HTTP_200_OK)
@inject
async def update_product(product: ProductEdit, ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    return await ibay_service.update_product(product)


@app.post('/buy_product', status_code=status.HTTP_200_OK)
@inject
async def remove_product(buy: BuyProduct, ibay_service: IBayService = Depends(Provide[Container.ibay_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await ibay_service.buy_product(buy, user_id)

