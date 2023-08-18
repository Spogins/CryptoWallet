from typing import Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.wallet.models import Transaction, Wallet


class ParserRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_trans_by_status(self, status):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).filter(Transaction.status == status))
            transactions = result.scalars().all()
            return [trans.hash for trans in transactions]

    async def get_wallets(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet))
            wallets = result.scalars().all()
            return [wallet.address for wallet in wallets]

