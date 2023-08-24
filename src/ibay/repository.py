from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.ibay.models import Product
from src.ibay.schemas import ProductForm, ProductEdit


class IBayRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def to_order(self, product_id):
        async with self.session_factory() as session:
            product: Product = await session.get(Product, product_id)
            if not product:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {product_id}")
            product.in_order = False
            await session.commit()
            await session.refresh(product)
            return product

    async def add(self, _product: ProductForm, user_id):
        try:
            async with self.session_factory() as session:
                product = Product(
                    title=_product.title,
                    image=_product.image,
                    price=_product.price,
                    wallet=_product.wallet,
                    user_id=user_id
                )
                session.add(product)
                await session.commit()
                await session.refresh(product)
                return product
        except:
            raise HTTPException(status_code=401,
                                detail='Wrong input data')

    async def get_all(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Product).where(Product.in_order == False))
            products = result.scalars().all()
            return products

    async def get(self, pr_id):
        async with self.session_factory() as session:
            product = await session.get(Product, pr_id)
            if product:
                return product
            else:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {pr_id}")

    async def update(self, _product: ProductEdit):
        async with self.session_factory() as session:
            product = await session.get(Product, _product.id)
            if not product:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {_product.id}")
            product.title = _product.title
            product.wallet = _product.wallet
            product.price = _product.price
            product.image = _product.image
            await session.commit()
            await session.refresh(product)
            return product

    async def remove_pr(self, pr_id):
        async with self.session_factory() as session:
            product = await session.get(Product, pr_id)
            if not product:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {pr_id}")
            await session.delete(product)
            await session.commit()


