from typing import Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.parser.models import Block
from src.wallet.models import Wallet, Asset


class WebRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_old_block(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            block = result.scalars().first()
            return block.number

    async def update_block(self, number: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            block: Block = result.scalars().first()
            block.number = number
            await session.commit()
            await session.refresh(block)

    async def get_asset(self, from_address, to_address):
        async with self.session_factory() as session:
            try:
                from_address = await session.execute(select(Wallet).where(Wallet.address == from_address))
                result_from = from_address.scalars().first()
                if from_address:
                    asset = await session.get(Asset, result_from.asset_id)
                return asset
            except:
                to_address = await session.execute(select(Wallet).where(Wallet.address == to_address))
                result_to = to_address.scalars().first()

                if to_address:
                    asset = await session.get(Asset, result_to.asset_id)
                    return asset
            finally:
                result = await session.execute(select(Asset))
                asset = result.scalars().first()
                return asset