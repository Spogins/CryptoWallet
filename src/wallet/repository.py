from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.wallet.models import Wallet, Blockchain, Asset


class WalletRepository:
    def __init__(self, session_factory: AsyncSession) -> None:
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




