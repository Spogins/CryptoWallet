import httpx
from eth_account import Account
from fastapi import HTTPException
from web3 import Web3, HTTPProvider

from config.settings import QUICKNODE_URL, MORALIS_API_KEY


class WebService:
    w3 = Web3(HTTPProvider(QUICKNODE_URL))
    moralis_api_key = MORALIS_API_KEY
    headers = {
        "X-API-Key": moralis_api_key
    }

    async def get_transactions(self, address):
        url = f'https://deep-index.moralis.io/api/v2/{address}/?chain=sepolia'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                transactions_data = response.json()
                result = transactions_data.get('result')
                transactions_list = []
                for trans in result:
                    transactions_list.append(trans)
                return transactions_list
            else:
                # print("Ошибка при запросе к Moralis API:", response.status_code)
                raise HTTPException(status_code=401, detail=f"Ошибка при запросе к Moralis API:, {response.status_code}")

    async def get_transaction(self, trans_hash):
        url = f'https://deep-index.moralis.io/api/v2/transaction/{trans_hash}?chain=sepolia'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                trans = response.json()
                return trans
            else:
                # print("Ошибка при запросе к Moralis API:", response.status_code)
                raise HTTPException(status_code=401,
                                    detail=f"Ошибка при запросе к Moralis API:, {response.status_code}")

    async def transaction_info(self, tx_hash):
        tx = self.w3.eth.get_transaction(tx_hash)
        tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)

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
            'Сумма': self.w3.from_wei(tx.value, 'ether'),
            'Статус': status
        }
        return tx_info


    async def get_balance(self, address):
        balance_wei = self.w3.eth.get_balance(address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        return {"address": address, "balance_eth": balance_eth}

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
            nonce = self.w3.eth.get_transaction_count(sender_address)
            # Создание транзакции
            transaction = {
                'to': receiver_address,
                'value': self.w3.to_wei(value, 'ether'),  # Сумма для перевода в Wei (0.1 ETH)
                'gas': 21000,  # Лимит газа для базовой транзакции
                'gasPrice': self.w3.to_wei('50', 'gwei'),  # Цена газа в Wei
                'nonce': nonce,
                'chainId': self.w3.eth.chain_id,  # ID сети (Ropsten)
            }
            # Подпись транзакции с использованием приватного ключа
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key_sender)
            # Отправка транзакции на блокчейн
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            # return {'tx_hash': tx_hash.hex()}
            trans_data = {
                "hash": tx_hash.hex(),
                "from_address": sender_address,
                "to_address": receiver_address,
                "value": value,
            }
            return trans_data
        except:
            raise HTTPException(status_code=401,
                                detail='Something went wrong, please make sure you entered the correct details and/or you have enough funds to complete the transaction.')