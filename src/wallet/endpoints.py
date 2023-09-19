from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Params, Page, paginate
from propan import RabbitBroker
from starlette import status

from config.settings import RABBITMQ_URL
from config_fastapi.fastapi_mgr import fastapi_mgr
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.wallet.containers import Container
from src.wallet.schemas import Transaction, TransForm
from src.wallet.models import Transaction as TransactionModel
from src.wallet.services.wallet import WalletService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


# bearer: HTTPAuthorizationCredentials = Depends(user_auth)
# @app.get("/tests_w")
# @inject
# async def test(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     await wallet_service.refund(120)

@app.get("/tests_wallets", status_code=status.HTTP_200_OK)
@inject
async def tests_wallets(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):

    # await fastapi_mgr.emit(event='transaction_info', data={'wallet': 'wallet',
    #                                                        'hash': 'hash',
    #                                                        'received': 'received',
    #                                                        'withdrawn': 'withdrawn'
    #                                                        }, room=15)

    async with RabbitBroker(RABBITMQ_URL) as broker:
        await broker.publish(message='test', queue='socketio/test')


    a_wallet = {
        "private_key": "0x17f270e0a153579b024b38a35ed11397e4b1a56c36f55b144d477ca1869f432e",
        "address": "0x44fe49b6c180B660933548A8632bE93079010F28"
    }

    b_wallet = {
        "private_key": "0xd150efcd2ac62da276c1ff5ad1449bedd336209b1d7861b0672cea57ab473568",
        "address": "0x5A79fe36275B1A8d557A8e1b3D36261515d12542"
    }

    c_wallet = {
        "private_key": "0xe0282cec5644e6981cfe402f8b9a1d58bd535c69aef14d3444e6244d09534af5",
        "address": "0x669130e74FB677D6616315D1CaE8c88BA4A883Df"
    }
    return {'a_wallet': a_wallet, 'b_wallet': b_wallet, 'c_wallet': c_wallet}


# @app.get("/generate_wallet", status_code=status.HTTP_200_OK)
# @inject
# async def generate_wallet(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.generate_wallet()


@app.get('/user_wallets', status_code=status.HTTP_200_OK)
@inject
async def user_wallets(user: int, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    # user_id = await get_user_from_bearer(bearer)
    return await wallet_service.user_wallets(user)


@app.get('/get_wallet/{wallet_id}', status_code=status.HTTP_200_OK)
@inject
async def get_wallet(wallet_id: int, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_wallet(wallet_id)


# @app.get('/get_wallet_by_address', status_code=status.HTTP_200_OK)
# @inject
# async def get_wallet_by_address(address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.get_wallet_by_address(address)


@app.post("/create_eth_wallet", status_code=status.HTTP_201_CREATED)
@inject
async def create_eth_wallet(wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.create_user_wallet(user_id)


@app.post("/import_eth_wallet", status_code=status.HTTP_201_CREATED)
@inject
async def import_eth_wallet(private_key: str,
                            wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.import_user_wallet(user_id, private_key)


@app.get("/wallet_balance", status_code=status.HTTP_200_OK)
@inject
async def wallet_balance(wallet_address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                         bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.get_balance(wallet_address)


@app.put("/update_wallet_balance", status_code=status.HTTP_200_OK)
@inject
async def update_wallet_balance(wallet_address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.update_balance(wallet_address)


@app.put("/update_all_wallets_balance", status_code=status.HTTP_200_OK)
@inject
async def update_all_wallets_balance(wallet_service: WalletService = Depends(Provide[Container.wallet_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.update_all(user_id)


@app.post("/test_trans", status_code=status.HTTP_201_CREATED)
@inject
async def send_eth(trans: Transaction,
                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.test_transaction(private_key_sender=trans.private_key_sender,
                                            receiver_address=trans.receiver_address, value=trans.value)


@app.post("/send_eth", status_code=status.HTTP_201_CREATED)
@inject
async def send_eth(trans: Transaction,
                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.transaction(from_address=trans.from_address,
                                            to_address=trans.to_address, value=trans.value)


@app.get('/wallet_db_transactions', status_code=status.HTTP_200_OK)
@inject
async def db_transactions(address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    transactions = await wallet_service.get_db_transaction(address)
    transactions = transactions[::-1]
    return transactions


@app.get('/db_transactions', status_code=status.HTTP_200_OK)
@inject
async def get_all_transaction(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_all_transaction()


# @app.put('/update_db_transaction', status_code=status.HTTP_200_OK)
# @inject
# async def transaction_update(_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.create_or_update(_hash)


# @app.put('/update_db_transactions', status_code=status.HTTP_200_OK)
# @inject
# async def update_all_transaction(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.update_all_transaction()


# @app.get('/transaction_info_web3', status_code=status.HTTP_200_OK)
# @inject
# async def transaction_info(_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.transaction_info(_hash)


@app.get('/transactions_moralis', status_code=status.HTTP_200_OK)
@inject
async def get_transactions(address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_transactions(address)

#
# @app.get('/transaction_w3', status_code=status.HTTP_200_OK)
# @inject
# async def get_by_hash(trans_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
#     return await wallet_service.get_transaction(trans_hash)


#CREATE ASSEY/BLOCKCHAIN MODEL
@app.post('/create_eth_asset', status_code=status.HTTP_201_CREATED)
@inject
async def create_eth_asset(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.create_eth()




