from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Cookie
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.wallet.containers import Container
from src.wallet.schemas import Wallet, Transaction
from src.wallet.services.wallet import WalletService

app = APIRouter()

user_auth = AutoModernJWTAuth()


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
    return {'a_wallet': a_wallet, 'b_wallet': b_wallet}


@app.post("/wallet_balance")
@inject
async def wallet_balance(wallet: Wallet, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_balance(wallet.wallet_address)


@app.post("/transaction")
@inject
async def wallet_balance(trans: Transaction,
                         wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.transaction(private_key_sender=trans.private_key_sender,
                                            receiver_address=trans.receiver_address, value=trans.value)


@app.get("/generate_wallet")
@inject
async def generate_wallet(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.generate_wallet()
