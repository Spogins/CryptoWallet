from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
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

    async def get_all_trans(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction))
            transactions = result.scalars().all()
            return transactions

    async def get_wallet(self, wallet_id):
        async with self.session_factory() as session:
            wallet = await session.get(Wallet, wallet_id)
            return wallet

    async def get_wallets(self):
        async with self.session_factory() as session:
            wallet = await session.execute(select(Wallet))
            wallets = wallet.scalars().all()
            return wallets

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
                return {'id': int(wallet.id), 'wallet': wallet.address, 'balance': float(wallet.balance)}
            else:
                raise HTTPException(status_code=401,
                                    detail='not a valid wallet make sure you check your wallet.')

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
            asset = Asset(abbreviation='ether', symbol='Ξ', decimal_places=18, blockchain=_blockchain)
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
                status=trans_data.get('status') if trans_data.get('status') else "PENDING",
                date=trans_data.get('age') if trans_data.get('age') else "PENDING",
                txn_fee=trans_data.get('txn_fee') if trans_data.get('txn_fee') else 0
            )
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return {'transaction': transaction}

    async def transaction_update(self, trans_data):
        async with self.session_factory() as session:
            result = await session.execute(select(Transaction).where(Transaction.hash == trans_data.get('hash')))
            transaction = result.scalar_one()

            transaction.status = trans_data.get('status')
            transaction.date = trans_data.get('age')
            transaction.txn_fee = trans_data.get('txn_fee')

            await session.commit()
            await session.refresh(transaction)
            return {'transaction': transaction}

    async def get_asset(self, from_address, to_address):
        async with self.session_factory() as session:

            from_address = await session.execute(select(Wallet).where(Wallet.address == from_address))
            to_address = await session.execute(select(Wallet).where(Wallet.address == to_address))

            result_from = from_address.scalars().first()
            result_to = to_address.scalars().first()

            if from_address:
                asset = await session.get(Asset, result_from.asset_id)
                return asset

            elif to_address:
                asset = await session.get(Asset, result_to.asset_id)
                return asset
            else:
                return False







