from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter
from starlette import status
from src.ibay.containers import Container
from src.ibay.schemas import ProductForm, ProductEdit
from src.ibay.services.ibay import IBayService

app = APIRouter()


@app.post('/add_product', status_code=status.HTTP_201_CREATED)
@inject
async def add_product(product: ProductForm, ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    return await ibay_service.add_product(product)


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


@app.delete('/delete_product', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_product(product: int, ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    return await ibay_service.remove_product(product)
