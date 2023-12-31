from datetime import datetime
from decimal import Decimal
from eth_account import Account
import secrets
from fastapi import HTTPException
from propan import RabbitBroker
from web3.exceptions import InvalidAddress
from config.settings import RABBITMQ_URL
from src.wallet.models import Asset, Wallet, Transaction
from src.wallet.repository import WalletRepository
from src.web3.w3_service import WebService


class WalletService:

    def __init__(self, wallet_repository: WalletRepository, w3_service: WebService) -> None:
        self._repository: WalletRepository = wallet_repository
        self.w3_service: WebService = w3_service

    async def load_wallet_trans(self, address):
        trans_list = await self.get_transactions(address)
        for trans_data in trans_list:
            await self._repository.create_or_update(trans_data)


    async def buy_product(self, data):
        from_wallet: Wallet = await self.get_wallet_by_address(data.get('from_wallet'))
        transaction: Transaction = await self.transaction(from_wallet.address, data.get('to_wallet'),
                                                          Decimal(data.get('value')))
        data: dict = {'transaction_id': transaction.id, 'product_id': data.get('product_id'),
                      'user_id': data.get('user_id')}
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='delivery/create_order')

    async def refund(self, _data):
        trans: Transaction = await self._repository.get_transaction(_data.get('trans_id'))
        wallet: Wallet = await self._repository.get_wallet_by_address(trans.to_address)
        value = trans.value + (Decimal(trans.txn_fee) * Decimal('1.5'))
        transaction: Transaction = await self.transaction(wallet.address, trans.from_address, value)
        data = {'transaction_id': _data.get('trans_id'), 'ref_transaction_id': transaction.id}
        if _data.get('status') == 'REFUND':
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message=data, queue='delivery/refund_transaction')

    async def get_wallet(self, wallet_id):
        return await self._repository.get_wallet(wallet_id)

    async def get_wallet_by_address(self, address):
        return await self._repository.get_wallet_by_address(address)

    async def create_user_wallet(self, user_id):
        wallet = await self.generate_wallet()
        return await self._repository.user_add_wallet(user_id, wallet)

    async def get_db_transaction(self, address):
        return await self._repository.get_db_transaction(address.lower())

    async def user_wallets(self, user_id):
        return await self._repository.user_wallets(user_id)

    async def get_all_transaction(self):
        return await self._repository.get_all_trans()

    async def import_user_wallet(self, user_id, private_key):
        try:
            account = Account.from_key(private_key)
            address = account.address
            wallet = {
                "private_key": private_key,
                "address": address
            }
            balance = await self.get_balance(address)
            balance = balance.get('balance_eth')
            return await self._repository.user_add_wallet(user_id, wallet, balance)
        except ValueError:
            raise HTTPException(status_code=401,
                                detail='Wrong input data.')

    async def parse_trans_data(self, trans, block_time, status, _hash):
        asset = await self.get_wallet_asset(trans.get('from'), trans.get('to'))
        gas_price_gwei = int(trans.get('gasPrice'))  # Пример: 100 Gwei
        gas_limit = int(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
        txn_fee_wei = gas_price_gwei * gas_limit * 10 ** (asset.decimal_places / 2)  # 1 Gwei = 10^9 Wei
        txn_fee_eth = txn_fee_wei / 10 ** asset.decimal_places

        if status == 1:
            status = "SUCCESS"
        elif status == 0:
            status = "FAILURE"
        else:
            status = "PENDING"
        value = Decimal((trans.get('value') / 10 ** asset.decimal_places))
        txn_fee = Decimal(txn_fee_eth / 10 ** (asset.decimal_places / 2))
        transaction = {
            "hash": _hash,
            "from_address": trans.get('from'),
            "to_address": trans.get('to'),
            "value": round(value, asset.decimal_places),
            "age": str(block_time),
            "txn_fee": round(txn_fee, asset.decimal_places),
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
        try:
            return await self.w3_service.get_balance(address)
        except InvalidAddress:
            raise HTTPException(status_code=401,
                                detail='Wrong input data.')

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
        try:
            balance = await self.w3_service.get_balance(address)
            return await self._repository.update_wallet_balance(address, balance.get('balance_eth'))
        except InvalidAddress:
            raise HTTPException(status_code=401,
                                detail='Wrong input data.')

    async def test_transaction(self, private_key_sender, receiver_address, value):
        trans_data = await self.w3_service.transaction(private_key_sender, receiver_address, value)
        return trans_data

    async def transaction(self, from_address, to_address, value):
        try:
            wallet = await self._repository.get_wallet_by_address(from_address)
            private_key_sender = wallet.private_key
            trans_data = await self.w3_service.transaction(private_key_sender, to_address, value)

            transaction = await self._repository.create_or_update(trans_data)
            await self.update_transactions_table(from_address, to_address)
            return transaction
        except:
            raise HTTPException(status_code=401,
                                detail='Wrong wallet data or value.')

    async def transaction_info(self, tx_hash):
        return await self.w3_service.transaction_info(tx_hash)

    async def send_transaction_status(self, trans_id, status):
        data = {
            'transaction_id': trans_id,
            'status': status
        }
        order_transaction = await self._repository.get_order_transaction(trans_id, False)
        if order_transaction is not None:
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message=data, queue='delivery/transaction_status')
            return

        ref_transaction = await self._repository.get_order_transaction(trans_id, True)
        if ref_transaction is not None:
            async with RabbitBroker(RABBITMQ_URL) as broker:
                data = {
                    'refund_id': trans_id,
                    'status': "REFUND"
                }
                await broker.publish(message=data, queue='delivery/refund_status')
            return

    async def create_or_update(self, _hash):
        trans_hash = await self.w3_service.get_transaction(_hash)
        trans_data = await self.parse_trans_data(trans_hash.get('transaction'), trans_hash.get('timestamp'),
                                                 trans_hash.get('status'), _hash)
        value = trans_data.get('value')
        transaction = await self._repository.create_or_update(trans_data)

        if not transaction.status == "PENDING":
            await self.update_transactions_table(trans_data.get('from_address'), trans_data.get('to_address'))
            await self.send_transaction_info(trans_data.get('from_address'), trans_data.get('to_address'), _hash, value)
            await self.send_transaction_status(transaction.id, transaction.status)
            await self.update_wallet_balance(trans_data.get('from_address'), trans_data.get('to_address'))
        return transaction

    async def update_transactions_table(self, from_address, to_address):
        wallets = [from_address, to_address]
        for address in wallets:
            wallet = await self._repository.check_wallet(address)
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message={'address': wallet.address, 'room': wallet.user.id}, queue='socketio/update_transactions_table')

    async def send_transaction_info(self, from_address, to_address, _hash, value):
        from_address = await self._repository.check_wallet(from_address)
        to_address = await self._repository.check_wallet(to_address)
        if from_address:
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message={'wallet': from_address.address,
                                              'hash': _hash,
                                              'received': False,
                                              'withdrawn': value,
                                              'room': from_address.user.id
                                              }, queue='socketio/send_notification')
        if to_address:
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message={'wallet': to_address.address,
                                              'hash': _hash,
                                              'received': value,
                                              'withdrawn': False,
                                              'room': to_address.user.id
                                              }, queue='socketio/send_notification')

    async def get_wallet_asset(self, from_address, to_address):
        asset = await self._repository.get_asset(from_address, to_address)
        if asset:
            return asset
        else:
            raise HTTPException(status_code=401,
                                detail='Not found asset for wallet.')

    async def update_wallet_balance(self, from_address, to_address):
        wallets = [from_address, to_address]
        for address in wallets:
            if await self._repository.check_wallet(address):
                wallet = await self.update_balance(address)
                async with RabbitBroker(RABBITMQ_URL) as broker:
                    await broker.publish(message={'address': wallet.get('wallet'), 'room': wallet.get('user'),
                                                  'balance': wallet.get('balance')}, queue='socketio/update_balance')


    #

    # USED ONLY FOR MORALIS TEST
    async def parse_trans_data_moralis(self, trans):
        current_time = datetime.utcnow()
        past_time = datetime.strptime(trans.get('block_timestamp'), "%Y-%m-%dT%H:%M:%S.%fZ")
        time_difference = current_time - past_time
        # Получение количества дней, часов, минут и секунд
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        gas_price_gwei = float(trans.get('gas_price'))  # Пример: 100 Gwei
        gas_limit = float(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
        txn_fee_wei = gas_price_gwei * gas_limit * 10 ** 9  # 1 Gwei = 10^9 Wei
        txn_fee_eth = txn_fee_wei / 10 ** 18

        if trans.get('receipt_status') == '1':
            status = "SUCCESS"
        elif trans.get('receipt_status') == '0':
            status = "FAILURE"
        else:
            status = "PENDING"



        # Форматирование объекта datetime в требуемый формат "2023-09-19 18:06:48"
        output_datetime_str = past_time.strftime("%Y-%m-%d %H:%M:%S")

        transaction = {
            "hash": trans.get('hash'),
            "from_address": trans.get('from_address'),
            "to_address": trans.get('to_address'),
            "value": float(trans.get('value')) / 10 ** 18,
            "age": output_datetime_str,
            "txn_fee": txn_fee_eth / 10 ** 9,
            'status': status
        }
        return transaction


    async def create_eth(self):
        return await self._repository.create_eth()
    #

    async def get_transactions(self, address):
        result = await self.w3_service.get_transactions(address)
        transactions_list = []
        for trans in result:
            transaction = await self.parse_trans_data_moralis(trans)
            transactions_list.append(transaction)
        return transactions_list

