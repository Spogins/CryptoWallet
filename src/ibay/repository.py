from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.ibay.models import Product
from src.ibay.schemas import ProductForm, ProductEdit, ProductsForm, AddProductForm
from src.wallet.models import Wallet


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
                    wallet_id=_product.wallet,
                    user_id=user_id
                )
                session.add(product)
                await session.commit()
                await session.refresh(product)
                result = await session.execute(select(Wallet).where(Wallet.id == _product.wallet))
                wallet: Wallet = result.scalar_one_or_none()
                return AddProductForm(
                    id=product.id,
                    title=product.title,
                    wallet=wallet.address,
                    price=product.price,
                    image=product.image
                )
        except:
            raise HTTPException(status_code=401,
                                detail='Wrong input data')

    async def get_all(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Product).options(joinedload(Product.wallet)))
            products = result.scalars().all()
            return [ProductsForm(
                id=product.id,
                title=product.title,
                wallet=product.wallet.address,
                price=product.price,
                image=product.image) for product in products]

    async def get(self, pr_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Product).options(joinedload(Product.wallet)).where(Product.id == pr_id))
            product = result.scalar_one_or_none()
            if product:
                return ProductsForm(
                    id=product.id,
                    title=product.title,
                    wallet=product.wallet.address,
                    price=product.price,
                    image=product.image)
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
            product.wallet_id = _product.wallet
            product.price = _product.price
            product.image = _product.image
            await session.commit()
            await session.refresh(product)
            return product



