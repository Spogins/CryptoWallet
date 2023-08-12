from datetime import datetime
import hexbytes
import httpx
from config.settings import MORALIS_API_KEY
from src.wallet.repository import WalletRepository
from src.wallet.services.test import w3


class ParserService:
    moralis_api_key = MORALIS_API_KEY
    headers = {
        "X-API-Key": moralis_api_key
    }

    def __init__(self, wallet_repository: WalletRepository) -> None:
        self._repository: WalletRepository = wallet_repository

    async def test(self):
        return 'ddddddddd'

    async def get_pending_hash(self):
        transactions = await self._repository.get_trans_by_status("PENDING")
        if len(transactions):
            _trans = []
            for trans in transactions:
                _trans.append(await self.parse_block(trans.hash))
            return {'transactions': _trans}
        else:
            return {'message': 'transactions not found'}


    async def parse_block(self, _hash):
        block_data = w3.eth.get_block('latest')
        for transaction_block in block_data.transactions:
            if hexbytes.HexBytes(transaction_block).hex() == _hash:
                transaction = await self.get_and_update(_hash)
                if transaction:
                    return transaction
                else:
                    return {'message': 'Not Found.'}

    async def get_and_update(self, _hash):
        url = f'https://deep-index.moralis.io/api/v2/transaction/{_hash}?chain=sepolia'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                trans = response.json()
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
                return False



