import httpx
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Cookie
from fastapi.security import HTTPAuthorizationCredentials
from datetime import datetime
from config.settings import MORALIS_API_KEY
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.wallet.containers import Container
from src.wallet.schemas import Wallet, Transaction
from src.wallet.services.wallet import WalletService
import requests

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
    return {'a_wallet': a_wallet, 'b_wallet': b_wallet}


@app.post("/wallet_balance")
@inject
async def wallet_balance(wallet: Wallet, wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.get_balance(wallet.wallet_address)


@app.post("/send_eth")
@inject
async def send_eth(trans: Transaction,
                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.transaction(private_key_sender=trans.private_key_sender,
                                            receiver_address=trans.receiver_address, value=trans.value)


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


@app.get('/get_transactions')
async def get_transactions(address: str, limit: int = 10):
    moralis_api_key = MORALIS_API_KEY

    url = f'https://deep-index.moralis.io/api/v2/{address}/?chain=sepolia'
    headers = {
        "X-API-Key": moralis_api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            current_time = datetime.utcnow()
            transactions_data = response.json()
            result = transactions_data.get('result')
            transactions_list = []
            for trans in result:
                past_time = datetime.strptime(trans.get('block_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ")
                time_difference = current_time - past_time
                # Получение количества дней, часов, минут и секунд
                days = time_difference.days
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)


                gas_price_gwei = int(trans.get('gas_price'))  # Пример: 100 Gwei
                gas_limit = int(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
                txn_fee_wei = gas_price_gwei * gas_limit * 10 ** 9  # 1 Gwei = 10^9 Wei
                txn_fee_eth = txn_fee_wei / 10 ** 18

                transaction = {
                    "hash": trans.get('hash'),
                    "from_address": trans.get('from_address'),
                    "to_address": trans.get('to_address'),
                    "value": int(trans.get('value')) / 10**18,
                    "age": f"Прошло {days} дней, {hours} часов, {minutes} минут, {seconds} секунд.",
                    "txn_fee": txn_fee_eth / 10**9
                }
                transactions_list.append(transaction)
            return transactions_list[:limit]
        else:
            print("Ошибка при запросе к Moralis API:", response.status_code)
            return None


@app.post('/create_eth_asset')
@inject
async def create_eth_asset(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.create_eth()



@app.post('/add_blockchain')
@inject
async def add_blockchain(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.create_blockchain()


@app.post('/add_asset')
@inject
async def add_blockchain(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    return await wallet_service.create_asset()



