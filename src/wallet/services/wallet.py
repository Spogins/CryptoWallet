from web3 import Web3, HTTPProvider
from eth_account import Account
import secrets
from config.settings import QUICKNODE_URL
from src.wallet.repository import WalletRepository

w3 = Web3(HTTPProvider(QUICKNODE_URL))


class WalletService:
    def __init__(self, wallet_repository: WalletRepository) -> None:
        self._repository: WalletRepository = wallet_repository

    async def create_user_wallet(self, user_id):
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        wallet = {
            "private_key": private_key,
            "address": acct.address
        }
        return await self._repository.user_add_wallet(user_id, wallet)

    async def import_user_wallet(self, user_id, private_key):
        account = Account.from_key(private_key)
        address = account.address
        wallet = {
            "private_key": private_key,
            "address": address
        }
        balance_wei = w3.eth.get_balance(address)
        balance = w3.from_wei(balance_wei, 'ether')
        return await self._repository.user_add_wallet(user_id, wallet, balance)

    async def create_eth(self):
        return await self._repository.create_eth()

    async def create_blockchain(self):
        pass

    async def create_asset(self):
        pass

    @staticmethod
    async def generate_wallet():
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        return {"private_key": private_key, "address": acct.address}

    @staticmethod
    async def get_balance(address):
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return {"address": address, "balance_eth": balance_eth}

    @staticmethod
    async def transaction(private_key_sender, receiver_address, value):
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

        return {'tx_hash': tx_hash.hex()}
