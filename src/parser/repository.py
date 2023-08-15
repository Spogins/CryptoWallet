from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.parser.models import Block
from src.wallet.models import Transaction, Wallet
from utils.base.parse_data_transaction import parse_trans_data


class ParserRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def update_balance(self, address, balance_eth):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).filter(Wallet.address == address))
            wallet = result.scalars().first()
            if wallet:
                wallet.balance = balance_eth
                await session.commit()
                await session.refresh(wallet)


    async def get_block(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            block = result.scalars().first()
            return block.number

    async def update_block(self, number):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            block = result.scalars().first()
            block.number = number
            await session.commit()
            await session.refresh(block)

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

    async def update_trans(self, trans_data):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).where(Transaction.hash == trans_data.get('hash')))
            transaction = result.scalar_one()
            if trans_data.get('status') == 1:
                transaction.status = "SUCCESS"
            else:
                transaction.status = "FAILURE"
            transaction.date = trans_data.get('age')
            transaction.txn_fee = trans_data.get('txn_fee')
            await session.commit()
            await session.refresh(transaction)
            return {'transaction_update': transaction}

    async def add_trans(self, trans_data):

        async with self.session_factory() as session:
            if trans_data.get('status') == 1:
                status = "SUCCESS"
            elif trans_data.get('status') == 0:
                status = "FAILURE"
            else:
                status = "PENDING"
            transaction = Transaction(
                hash=trans_data.get('hash'),
                from_address=trans_data.get('from_address'),
                to_address=trans_data.get('to_address'),
                value=trans_data.get('value'),
                date=trans_data.get('age'),
                txn_fee=trans_data.get('txn_fee'),
                status=status
            )
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return {'new_transaction': transaction}
