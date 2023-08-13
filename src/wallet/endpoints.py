from time import sleep

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.wallet.containers import Container
from src.wallet.schemas import Transaction
from src.wallet.services.wallet import WalletService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


# bearer: HTTPAuthorizationCredentials = Depends(user_auth)


@app.get("/tests_wallets")
async def tests_wallets():
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


@app.get('/user_wallets')
@inject
async def user_wallets(user: int, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    # user_id = await get_user_from_bearer(bearer)
    return await wallet_service.user_wallets(user)


@app.get("/generate_wallet")
@inject
async def generate_wallet(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.generate_wallet()


@app.post("/create_eth_wallet")
@inject
async def create_eth_wallet(wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.create_user_wallet(user_id)


@app.post("/import_eth_wallet")
@inject
async def import_eth_wallet(private_key: str,
                            wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.import_user_wallet(user_id, private_key)


@app.get("/wallet_balance")
@inject
async def wallet_balance(wallet_address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                         bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.get_balance(wallet_address)


@app.put("/update_wallet_balance")
@inject
async def update_wallet_balance(wallet_address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                         bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.update_balance(wallet_address, user_id)


@app.put("/update_all_wallets_balance")
@inject
async def update_all_wallets_balance(user: int, wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                         bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    # user_id = await get_user_from_bearer(bearer)
    return await wallet_service.update_all(user)


@app.post("/send_eth")
@inject
async def send_eth(trans: Transaction,
                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):

    # return await wallet_service.transaction(private_key_sender=trans.private_key_sender,
    #                                         receiver_address=trans.receiver_address, value=trans.value)

    a_wallet = await wallet_service.transaction(private_key_sender='0x17f270e0a153579b024b38a35ed11397e4b1a56c36f55b144d477ca1869f432e',
                                              receiver_address="0x5A79fe36275B1A8d557A8e1b3D36261515d12542", value=0.01)


    c_wallet = await wallet_service.transaction(private_key_sender="0xd150efcd2ac62da276c1ff5ad1449bedd336209b1d7861b0672cea57ab473568",
                                              receiver_address='0x669130e74FB677D6616315D1CaE8c88BA4A883Df', value=0.001)

    return {'a_wallet': a_wallet, 'c_wallet': c_wallet}


@app.get('/get_transactions')
@inject
async def get_transactions(address: str, limit: int = 10, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_transactions(address, limit)


@app.get('/transaction_by_hash')
@inject
async def get_by_hash(trans_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_transaction(trans_hash)

@app.get('/db_transactionns')
@inject
async def db_transactionns(address: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_db_transaction(address)


@app.get('/transaction_info')
@inject
async def transaction_info(_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.transaction_info(_hash)


@app.put('/transaction_update')
@inject
async def transaction_update(_hash: str, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.transaction_update(_hash)


@app.put('/update_all_transaction')
@inject
async def update_all_transaction(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.update_all_transaction()



#CREATE ASSEY/BLOCKCHAIN MODEL
@app.post('/create_eth_asset')
@inject
async def create_eth_asset(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.create_eth()




