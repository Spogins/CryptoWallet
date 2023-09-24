import asyncio
import passlib.hash
from sqlalchemy import select

from src.core.containers import Container
from src.parser.models import Block
from src.users.models import User
from src.wallet.models import Asset, Blockchain

container = Container()
db = container.db()


async def password_hasher(password):
    hashed_psw = passlib.hash.pbkdf2_sha256.hash(password)
    return hashed_psw

async def block():
    print('Create model Block')
    async with db._session_factory() as session:
        _block = Block()
        session.add(_block)
        await session.commit()
        await session.refresh(_block)
    print('Block created')


async def blockchain_asset():
    print('Create blockchain_asset')
    async with db._session_factory() as session:
        blockchain = Blockchain(name='Ethereum', code='ethereum')
        session.add(blockchain)
        await session.commit()
        await session.refresh(blockchain)

    async with db._session_factory() as session:
        _blockchain = await session.execute(select(Blockchain).filter_by(name='Ethereum'))
        _blockchain = _blockchain.scalars().first()
        asset = Asset(abbreviation='ether', symbol='Ξ', decimal_places=18, blockchain=_blockchain,
                      image='https://upload.wikimedia.org/wikipedia/commons/6/6f/Ethereum-icon-purple.svg')
        session.add(asset)
        await session.commit()
        await session.refresh(asset)
        _asset = await session.execute(select(Asset).filter_by(abbreviation='ETH'))
        _asset = _asset.scalars().first()
    print('blockchain_asset created')



async def admin_user():
    print('Create Admin User')
    async with db._session_factory() as session:
        user = User(
            email='admin@admin.com',
            username='admin@admin',
            password=await password_hasher('AdminWallet5231'),
            is_superuser=True,
            is_active=True,
            chat_access=True,
            avatar='#'
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    print('Admin User created')


async def users():
    print('Create Users')
    async with db._session_factory() as session:
        for usr in range(2):
            user = User(
                email=f'user{usr + 1}@user.com',
                username=f'user0{usr + 1}',
                password=await password_hasher('UserWallet5231'),
                is_superuser=False,
                is_active=True,
                chat_access=True,
                avatar='#'
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f'User0{usr+1} created')
    print('Users created')


async def main():
    await block()
    await admin_user()
    await users()
    await blockchain_asset()



if __name__ == "__main__":
    asyncio.run(main())

