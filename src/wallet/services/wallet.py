from decimal import Decimal
from datetime import datetime
from typing import Type
from eth_account import Account
import secrets
from fastapi import HTTPException
from propan import RabbitBroker
from config.settings import RABBITMQ_URL
from src.wallet.models import Asset, Wallet, Transaction
from src.wallet.repository import WalletRepository
from src.web3.w3_service import WebService


class WalletService:

    def __init__(self, wallet_repository: WalletRepository, w3_service: WebService) -> None:
        self._repository: WalletRepository = wallet_repository
        self.w3_service: WebService = w3_service

    async def buy_product(self, data):
        from_wallet: Wallet = await self.get_wallet_by_address(data.get('from_wallet'))
        transaction = await self.transaction(from_wallet.private_key, data.get('to_wallet'), float(data.get('value')))
        trans: Transaction = transaction.get('transaction')
        data: dict = {'trans_id': trans.id, 'product_id': data.get('product_id')}
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='delivery/create_order')

    async def refund(self, trans_id):
        trans: Transaction = await self._repository.get_transaction(trans_id)
        wallet: Wallet = await self._repository.get_wallet_by_address(trans.to_address)
        value = trans.value + (Decimal(trans.txn_fee) * Decimal('1.5'))
        await self.transaction(wallet.private_key, trans.from_address, value)

    async def get_wallet(self, wallet_id):
        return await self._repository.get_wallet(wallet_id)

    async def get_wallet_by_address(self, address):
        return await self._repository.get_wallet_by_address(address)

    async def create_user_wallet(self, user_id):
        wallet = await self.generate_wallet()
        return await self._repository.user_add_wallet(user_id, wallet)

    async def get_db_transaction(self, address):
        return await self._repository.get_db_transaction(address)

    async def user_wallets(self, user_id):
        return await self._repository.user_wallets(user_id)

    async def get_all_transaction(self):
        return await self._repository.get_all_trans()

    async def import_user_wallet(self, user_id, private_key):
        account = Account.from_key(private_key)
        address = account.address
        wallet = {
            "private_key": private_key,
            "address": address
        }
        balance = await self.get_balance(address)
        balance = balance.get('balance_eth')
        return await self._repository.user_add_wallet(user_id, wallet, balance)

    async def parse_trans_data(self, trans, block_time, status, _hash):
        asset = await self.get_wallet_asset(trans.get('from'), trans.get('to'))
        gas_price_gwei = int(trans.get('gasPrice'))  # Пример: 100 Gwei
        gas_limit = int(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
        txn_fee_wei = gas_price_gwei * gas_limit * 10 ** (asset.decimal_places/2)  # 1 Gwei = 10^9 Wei
        txn_fee_eth = txn_fee_wei / 10 ** asset.decimal_places

        if status == 1:
            status = "SUCCESS"
        elif status == 0:
            status = "FAILURE"
        else:
            status = "PENDING"

        transaction = {
            "hash": _hash,
            "from_address": trans.get('from'),
            "to_address": trans.get('to'),
            "value": Decimal((trans.get('value')) / 10 ** asset.decimal_places),
            "age": str(block_time),
            "txn_fee": txn_fee_eth / 10 ** (asset.decimal_places/2),
            'status': status
        }
        return transaction

    async def get_transaction(self, _hash):
        transaction = await self.w3_service.get_transaction(_hash)
        return await self.parse_trans_data(transaction.get('transaction'), transaction.get('timestamp'),
                                           transaction.get('status'), _hash)

    @staticmethod
    async def generate_wallet():
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        return {"private_key": private_key, "address": acct.address}

    async def get_balance(self, address):
        return await self.w3_service.get_balance(address)

    async def update_all(self, user_id):
        wallets = await self._repository.get_wallets(user_id)
        u_balance = []
        for wallet in wallets:
            address = wallet.address
            balance = await self.get_balance(address)
            updated = await self._repository.update_wallet_balance(address, balance.get('balance_eth'))
            u_balance.append(updated)
        return u_balance

    async def update_balance(self, address):
        balance = await self.w3_service.get_balance(address)
        return await self._repository.update_wallet_balance(address, balance.get('balance_eth'))

    async def test_transaction(self, private_key_sender, receiver_address, value):
        trans_data = await self.w3_service.transaction(private_key_sender, receiver_address, value)
        return trans_data

    async def transaction(self, private_key_sender, receiver_address, value):
        trans_data = await self.w3_service.transaction(private_key_sender, receiver_address, value)
        return await self._repository.create_or_update(trans_data)

    async def transaction_info(self, tx_hash):
        return await self.w3_service.transaction_info(tx_hash)

    @staticmethod
    async def send_transaction_status(trans_id, _hash, status):
        if not status == "PENDING":
            data = {
                'trans_id': trans_id,
                'hash': _hash,
                'status': status
            }
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message=data, queue='delivery/transaction_status')

    async def create_or_update(self, _hash):
        trans_hash = await self.w3_service.get_transaction(_hash)
        trans_data = await self.parse_trans_data(trans_hash.get('transaction'), trans_hash.get('timestamp'),
                                                 trans_hash.get('status'), _hash)
        value = trans_data.get('value')
        transaction = await self._repository.create_or_update(trans_data)
        await self.send_transaction_status(transaction.get('transaction').id, transaction.get('transaction').hash, transaction.get('transaction').status)
        await self.update_wallet_balance(trans_data.get('from_address'), trans_data.get('to_address'))
        return transaction

    async def get_wallet_asset(self, from_address, to_address):
        asset = await self._repository.get_asset(from_address, to_address)
        if asset:
            return asset
        else:
            raise HTTPException(status_code=401,
                                detail='Not found asset for wallet.')

    async def update_wallet_balance(self, from_address, to_address):
        if await self._repository.check_wallet(from_address):
            await self.update_balance(from_address)
        if await self._repository.check_wallet(to_address):
            await self.update_balance(to_address)
    #
    #
    # # USED ONLY FOR MORALIS TEST
    # async def parse_trans_data_moralis(self, trans):
    #     current_time = datetime.utcnow()
    #     past_time = datetime.strptime(trans.get('block_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ")
    #     time_difference = current_time - past_time
    #     # Получение количества дней, часов, минут и секунд
    #     days = time_difference.days
    #     hours, remainder = divmod(time_difference.seconds, 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #
    #     gas_price_gwei = float(trans.get('gas_price'))  # Пример: 100 Gwei
    #     gas_limit = float(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
    #     txn_fee_wei = gas_price_gwei * gas_limit * 10 ** 9  # 1 Gwei = 10^9 Wei
    #     txn_fee_eth = txn_fee_wei / 10 ** 18
    #     transaction = {
    #         "hash": trans.get('hash'),
    #         "from_address": trans.get('from_address'),
    #         "to_address": trans.get('to_address'),
    #         "value": float(trans.get('value')) / 10 ** 18,
    #         "age": f"Прошло {days} дней, {hours} часов, {minutes} минут, {seconds} секунд.",
    #         "txn_fee": txn_fee_eth / 10 ** 9,
    #         'block_number': trans.get('block_number'),
    #         "status": trans.get('receipt_status'),
    #     }
    #     return transaction

    #
    #
    #
    # async def update_all_transaction(self):
    #     all_trans = await self._repository.get_all_trans()
    #     updated = []
    #     for trans in all_trans:
    #         updated_trans = await self.create_or_update(trans.hash)
    #         updated.append(updated_trans)
    #     return updated
    #
    #
    #
    # async def create_eth(self):
    #     return await self._repository.create_eth()
    #

    # async def get_transactions(self, address, limit):
    #     result = await self.w3_service.get_transactions(address)
    #     transactions_list = []
    #     for trans in result:
    #         transaction = await self.parse_trans_data_moralis(trans)
    #         transactions_list.append(transaction)
    #     return transactions_list[:limit]
    #