from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import w3
from src.users.models import User
from src.wallet.models import Wallet, Blockchain, Asset, Transaction
from src.wallet.schemas import UserWallet


class WalletRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def user_add_wallet(self, user_id, wallet, balance: float = 0):
        try:
            async with self.session_factory() as session:
                _asset = await session.execute(select(Asset).filter_by(abbreviation='ETH'))
                _asset = _asset.scalars().first()
                user = await session.get(User, user_id)
                _wallet = Wallet(private_key=wallet.get('private_key'), address=wallet.get('address'), user=user, asset=_asset, balance=balance)
                session.add(_wallet)
                await session.commit()
                await session.refresh(_wallet)
                return _wallet
        except:
            raise HTTPException(status_code=401, detail='the wallet was registered on the account earlier make sure you are using a new or empty wallet')

    # async def get_trans_by_status(self, status):
    #     async with self.session_factory() as session:
    #         result = await session.execute(select(Transaction).filter(Transaction.status == status))
    #         transactions = result.scalars().all()
    #         return transactions

    async def get_all_trans(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction))
            transactions = result.scalars().all()
            return transactions

    async def user_wallets(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            wallets = result.scalars().all()
            return [UserWallet(id=wallet.id, address=wallet.address, balance=wallet.balance) for wallet in wallets]

    async def update_wallet_balance(self, address, balance_eth, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.address == address and Wallet.user_id == user_id))
            wallet = result.scalar_one()
            if wallet:
                wallet.balance = balance_eth
                await session.commit()
                await session.refresh(wallet)
                return {'wallet': address, 'balance_eth': balance_eth}
            else:
                raise HTTPException(status_code=401,
                                    detail='not a valid wallet make sure you check your wallet.')

    async def update_all_wallets(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            wallets = result.scalars().all()
            for wallet in wallets:
                balance_wei = w3.eth.get_balance(wallet.address)
                balance_eth = w3.from_wei(balance_wei, 'ether')
                wallet.balance = balance_eth
                await session.commit()
                await session.refresh(wallet)
            return [UserWallet(id=wallet.id, address=wallet.address, balance=wallet.balance) for wallet in wallets]

    async def get_db_transaction(self, address):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).filter_by(from_address=address))
            transactions = result.scalars().all()
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
            asset = Asset(abbreviation='ETH', symbol='Ξ', blockchain=_blockchain)
            session.add(asset)
            await session.commit()
            await session.refresh(asset)
            _asset = await session.execute(select(Asset).filter_by(abbreviation='ETH'))
            _asset = _asset.scalars().first()
            return {'blockchain': _blockchain, 'asset': _asset}

    async def add_transaction(self, trans_data):
        async with self.session_factory() as session:
            transaction = Transaction(
                hash=trans_data.get('hash'),
                from_address=trans_data.get('from_address'),
                to_address=trans_data.get('to_address'),
                value=trans_data.get('value'),
            )
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return {'transaction': transaction}

    async def transaction_update(self, trans_data):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).where(Transaction.hash == trans_data.get('hash')))
            transaction = result.scalar_one()
            if trans_data.get('status') == '1':
                transaction.status = "SUCCESS"
            else:
                transaction.status = "FAILURE"
            transaction.date = trans_data.get('age')
            transaction.txn_fee = trans_data.get('txn_fee')

            await session.commit()
            await session.refresh(transaction)
            return {'transaction': transaction}






