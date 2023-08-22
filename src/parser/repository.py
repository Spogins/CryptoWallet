from typing import Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.wallet.models import Transaction, Wallet


class ParserRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_db_trans(self, _hash):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).where(Transaction.hash.in_(_hash)))
            trans = result.scalars().all()
            return [data.hash for data in trans]

    async def get_wallet(self, address):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.address.in_(address)))
            wallets = result.scalars().all()
            return [data.address for data in wallets]

