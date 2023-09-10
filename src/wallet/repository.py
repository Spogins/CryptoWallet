from typing import Callable, Type
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.delivery.models import Order
from src.users.models import User
from src.wallet.models import Wallet, Blockchain, Asset, Transaction
from src.wallet.schemas import UserWallet


class WalletRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_order_transaction(self, trans_id, refund):
        async with self.session_factory() as session:
            if not refund:
                transaction = await session.execute(select(Order).where(Order.transaction_id == trans_id))
            else:
                transaction = await session.execute(select(Order).where(Order.refund_id == trans_id))
            result = transaction.scalar_one_or_none()
            return result

    async def get_transaction(self, trans_id):
        async with self.session_factory() as session:
            transaction = await session.execute(select(Transaction).where(Transaction.id == trans_id))
            result = transaction.scalar_one_or_none()
            return result

    async def create_or_update(self, trans_data):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).where(Transaction.hash == trans_data.get('hash')))
            transaction = result.scalar_one_or_none()
            if transaction:
                transaction.status = trans_data.get('status')
                transaction.date = trans_data.get('age')
                transaction.txn_fee = trans_data.get('txn_fee')
            else:
                transaction = Transaction(
                    hash=trans_data.get('hash'),
                    from_address=trans_data.get('from_address'),
                    to_address=trans_data.get('to_address'),
                    value=trans_data.get('value'),
                    status=trans_data.get('status') if trans_data.get('status') else "PENDING",
                    date=trans_data.get('age') if trans_data.get('age') else "PENDING",
                    txn_fee=trans_data.get('txn_fee') if trans_data.get('txn_fee') else 0
                )
                session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return transaction

    async def user_add_wallet(self, user_id, wallet, balance: float = 0):

        async with self.session_factory() as session:
            _asset = await session.execute(select(Asset).filter_by(abbreviation='ether'))
            _asset = _asset.scalars().first()
            user = await session.get(User, user_id)
            _wallet = Wallet(private_key=wallet.get('private_key'), address=wallet.get('address'), user=user, asset=_asset, balance=balance)
            try:
                session.add(_wallet)
                await session.commit()
                await session.refresh(_wallet)
                return UserWallet(id=_wallet.id, address=_wallet.address, balance=_wallet.balance, asset_img=_wallet.asset.image)
            except:
                raise HTTPException(status_code=401, detail='The wallet was registered on the account earlier make sure you are using a new or empty wallet')

    async def get_all_trans(self, limit: int = 10):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).limit(limit))
            transactions = result.scalars().all()
            return transactions

    async def get_wallet(self, wallet_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.id == wallet_id))
            wallet: Wallet = result.scalar_one_or_none()
            if not wallet:
                raise HTTPException(status_code=401,
                                    detail=f"Wallet not found, id: {wallet_id}")
            return UserWallet(id=wallet.id, address=wallet.address, balance=wallet.balance)

    async def get_wallet_by_address(self, address):
        async with self.session_factory() as session:
            wallet = await session.execute(select(Wallet).where(Wallet.address == address))
            wallet = wallet.scalars().first()
            return wallet


    async def get_wallets(self, user_id):
        async with self.session_factory() as session:
            wallet = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            wallets = wallet.scalars().all()
            return wallets

    async def user_wallets(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).options(joinedload(Wallet.asset)).where(Wallet.user_id == user_id))
            wallets = result.scalars().all()
            return [UserWallet(id=wallet.id, address=wallet.address, balance=wallet.balance, asset_img=wallet.asset.image) for wallet in wallets]

    async def update_wallet_balance(self, address, balance_eth):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.address == address))
            wallet = result.scalar_one()
            if wallet:
                wallet.balance = balance_eth
                await session.commit()
                await session.refresh(wallet)
                return {'id': int(wallet.id), 'wallet': wallet.address, 'balance': float(wallet.balance)}
            else:
                raise HTTPException(status_code=401,
                                    detail='not a valid wallet make sure you check your wallet.')

    async def get_db_transaction(self, address, limit: int = 10):
        async with self.session_factory() as session:
            result_from = await session.execute(select(Transaction).where(Transaction.from_address == address).limit(limit))
            result_to = await session.execute(select(Transaction).where(Transaction.to_address == address).limit(limit))
            transactions: list = result_from.scalars().all()
            transactions_to = result_to.scalars().all()
            transactions.extend(transactions_to)
            return transactions

    async def create_eth(self):
        async with self.session_factory() as session:
            blockchain = Blockchain(name='Ethereum', code='ethereum')
            session.add(blockchain)
            await session.commit()
            await session.refresh(blockchain)

        async with self.session_factory() as session:
            _blockchain = await session.execute(select(Blockchain).filter_by(name='Ethereum'))
            _blockchain = _blockchain.scalars().first()
            asset = Asset(abbreviation='ether', symbol='Ξ', decimal_places=18, blockchain=_blockchain, image='https://upload.wikimedia.org/wikipedia/commons/6/6f/Ethereum-icon-purple.svg')
            session.add(asset)
            await session.commit()
            await session.refresh(asset)
            _asset = await session.execute(select(Asset).filter_by(abbreviation='ETH'))
            _asset = _asset.scalars().first()
            return {'blockchain': _blockchain, 'asset': _asset}

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

    async def check_wallet(self, address):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.address == address).options(joinedload(Wallet.user)))
            wallet = result.scalar_one_or_none()
            if wallet is not None:
                return wallet
            else:
                return False






