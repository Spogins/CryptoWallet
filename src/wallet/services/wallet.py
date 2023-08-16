from datetime import datetime
import httpx
from eth_account import Account
import secrets
from fastapi import HTTPException
from config.settings import MORALIS_API_KEY, w3
from src.wallet.repository import WalletRepository


class WalletService:
    moralis_api_key = MORALIS_API_KEY
    headers = {
        "X-API-Key": moralis_api_key
    }

    def __init__(self, wallet_repository: WalletRepository) -> None:
        self._repository: WalletRepository = wallet_repository

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

    async def parse_trans_data(self, trans):
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
            'block_number': trans.get('block_number')
        }
        return transaction

    async def get_transactions(self, address, limit):
        url = f'https://deep-index.moralis.io/api/v2/{address}/?chain=sepolia'

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                transactions_data = response.json()
                result = transactions_data.get('result')
                transactions_list = []
                for trans in result:
                    transaction = await self.parse_trans_data(trans)
                    transactions_list.append(transaction)
                return transactions_list[:limit]
            else:
                print("Ошибка при запросе к Moralis API:", response.status_code)
                return None

    async def get_transaction(self, trans_hash):
        url = f'https://deep-index.moralis.io/api/v2/transaction/{trans_hash}?chain=sepolia'

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                trans = response.json()
                transaction = await self.parse_trans_data(trans)
                return transaction
            else:
                print("Ошибка при запросе к Moralis API:", response.status_code)
                return None

    @staticmethod
    async def generate_wallet():
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        return {"private_key": private_key, "address": acct.address}


    async def get_balance(self, address):
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return {"address": address, "balance_eth": balance_eth}

    async def update_all(self):
        return await self._repository.update_all_wallets()

    async def update_balance(self, address, user_id):
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return await self._repository.update_wallet_balance(address, balance_eth, user_id)

    async def transaction(self, private_key_sender, receiver_address, value):
        try:
            # Приватный ключ отправителя
            private_key_sender = private_key_sender
            # Адрес отправителя (получается из приватного ключа)
            sender_account = Account.from_key(private_key_sender)
            sender_address = sender_account.address
            # Адрес получателя
            receiver_address = receiver_address
            # Получение nonce для подписи транзакции
            nonce = w3.eth.get_transaction_count(sender_address)
            # Создание транзакции
            transaction = {
                'to': receiver_address,
                'value': w3.to_wei(value, 'ether'),  # Сумма для перевода в Wei (0.1 ETH)
                'gas': 21000,  # Лимит газа для базовой транзакции
                'gasPrice': w3.to_wei('50', 'gwei'),  # Цена газа в Wei
                'nonce': nonce,
                'chainId': w3.eth.chain_id,  # ID сети (Ropsten)
            }
            # Подпись транзакции с использованием приватного ключа
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key_sender)
            # Отправка транзакции на блокчейн
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            # return {'tx_hash': tx_hash.hex()}
            trans_data = {
                "hash": tx_hash.hex(),
                "from_address": sender_address,
                "to_address": receiver_address,
                "value": value,
            }
            return await self._repository.add_transaction(trans_data)
        except:
            raise HTTPException(status_code=401,
                                detail='Something went wrong, please make sure you entered the correct details and/or you have enough funds to complete the transaction.')

    async def create_eth(self):
        return await self._repository.create_eth()

    @staticmethod
    async def transaction_info(tx_hash):
        tx = w3.eth.get_transaction(tx_hash)
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)

        if tx_receipt is None:
            status = "Pending"
        elif tx_receipt['status'] == 1:
            status = "Success"
        else:
            status = "Failure"

        tx_info = {
            'Хэш транзакции': tx.hash.hex(),
            'Отправитель': tx['from'],
            'Получатель': tx['to'],
            'Сумма': w3.from_wei(tx.value, 'ether'),
            'Статус': status
        }
        return tx_info

    async def update_all_transaction(self):
        all_trans = await self._repository.get_all_trans()
        updated = []
        for trans in all_trans:
            updated_trans = await self.transaction_update(trans.hash)
            updated.append(updated_trans)
        return updated

    async def transaction_update(self, _hash):
        url = f'https://deep-index.moralis.io/api/v2/transaction/{_hash}?chain=sepolia'

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                trans = response.json()
                print(type(trans.get('receipt_status')))
                if trans.get('receipt_status') == '1' or trans.get('receipt_status') == '0':
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
                        'hash': trans.get('hash'),
                        "status": trans.get('receipt_status'),
                        "age": f"Прошло {days} дней, {hours} часов, {minutes} минут, {seconds} секунд.",
                        "txn_fee": txn_fee_eth / 10 ** 9
                    }
                    return await self._repository.transaction_update(transaction)
                else:
                    return {'message': 'No Changes'}
            else:
                print("Ошибка при запросе к Moralis API:", response.status_code)
            return None


