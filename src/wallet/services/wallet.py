from datetime import datetime
from eth_account import Account
import secrets
from src.wallet.repository import WalletRepository
from src.web3.w3_service import WebService


class WalletService:

    def __init__(self, wallet_repository: WalletRepository, w3_service: WebService) -> None:
        self._repository: WalletRepository = wallet_repository
        self.w3_service: WebService = w3_service

    async def get_wallet(self, wallet_id):
        return await self._repository.get_wallet(wallet_id)

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
        # current_time = datetime.utcnow()
        # past_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        # time_difference = current_time - past_time
        # # Получение количества дней, часов, минут и секунд
        # days = time_difference.days
        # hours, remainder = divmod(time_difference.seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)
        gas_price_gwei = int(trans.get('gasPrice'))  # Пример: 100 Gwei
        gas_limit = int(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
        txn_fee_wei = gas_price_gwei * gas_limit * 10 ** 9  # 1 Gwei = 10^9 Wei
        txn_fee_eth = txn_fee_wei / 10 ** 18

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
            "value": int(trans.get('value')) / 10 ** 18,
            "age": str(block_time),
            "txn_fee": txn_fee_eth / 10 ** 9,
            'status': status
        }
        return transaction

    async def get_transactions(self, address, limit):
        result = await self.w3_service.get_transactions(address)
        transactions_list = []
        for trans in result:
            transaction = await self.parse_trans_data_moralis(trans)
            transactions_list.append(transaction)
        return transactions_list[:limit]


    async def get_transaction(self, _hash):
        transaction = await self.w3_service.get_transaction(_hash)
        return await self.parse_trans_data(transaction.get('transaction'), transaction.get('timestamp'), transaction.get('status'), _hash)



    @staticmethod
    async def generate_wallet():
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        return {"private_key": private_key, "address": acct.address}

    async def get_balance(self, address):
        return await self.w3_service.get_balance(address)

    async def update_all(self):
        wallets = await self._repository.get_wallets()
        u_balance = []
        for wallet in wallets:
            address = wallet.address
            balance = await self.get_balance(address)
            updated = await self._repository.update_wallet_balance(address, balance.get('balance_eth'), wallet.user_id)
            u_balance.append(updated)
        return u_balance

    async def update_balance(self, address, user_id):
        balance = await self.w3_service.get_balance(address)
        return await self._repository.update_wallet_balance(address, balance.get('balance_eth'), user_id)

    async def transaction(self, private_key_sender, receiver_address, value):
        trans_data = await self.w3_service.transaction(private_key_sender, receiver_address, value)
        return await self._repository.add_transaction(trans_data)

    async def create_eth(self):
        return await self._repository.create_eth()

    async def transaction_info(self, tx_hash):
        return await self.w3_service.transaction_info(tx_hash)

    async def update_all_transaction(self):
        all_trans = await self._repository.get_all_trans()
        updated = []
        for trans in all_trans:
            updated_trans = await self.transaction_update(trans.hash)
            updated.append(updated_trans)
        return updated

    async def transaction_update(self, _hash):
        trans_hash = await self.w3_service.get_transaction(_hash)
        trans_data = await self.parse_trans_data(trans_hash.get('transaction'), trans_hash.get('timestamp'), trans_hash.get('status'), _hash)
        return await self._repository.transaction_update(trans_data)

    async def add_transaction(self, _hash):
        trans_hash = await self.w3_service.get_transaction(_hash)
        trans_data = await self.parse_trans_data(trans_hash.get('transaction'), trans_hash.get('timestamp'),
                                                 trans_hash.get('status'), _hash)
        return await self._repository.add_transaction(trans_data)


    async def parse_trans_data_moralis(self, trans):
        current_time = datetime.utcnow()
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
            "value": int(trans.get('value')) / 10 ** 18,
            "age": f"Прошло {days} дней, {hours} часов, {minutes} минут, {seconds} секунд.",
            "txn_fee": txn_fee_eth / 10 ** 9,
            'block_number': trans.get('block_number'),
            "status": trans.get('receipt_status'),
        }
        return transaction



