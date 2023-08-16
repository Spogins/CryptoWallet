import hexbytes
import httpx
from config.settings import MORALIS_API_KEY
from src.parser.repository import ParserRepository
from src.wallet.services.test import w3
from utils.base.parse_data_transaction import parse_trans_data


class ParserService:
    moralis_api_key = MORALIS_API_KEY
    headers = {
        "X-API-Key": moralis_api_key
    }
    block = 0
    hash_trans = []

    def __init__(self, parser_repository: ParserRepository) -> None:
        self._repository: ParserRepository = parser_repository


    @staticmethod
    async def forward_iterator(lst):
        for item in lst:
            yield item

    # async def get_block(self):
    #     self.block = await self._repository.get_block()
    #     block_latest = w3.eth.get_block('latest')
    #     block = w3.eth.get_block(self.block)
    #     if not block_latest == block:
    #         await self._repository.update_block(block_latest.number)
    #         print('---FIND_BLOCK---')
    #         print(f"---{block.number}---")
    #         return await self.parse_block(block)
    #     else:
    #         print('---SKIP_BLOCK---')

    async def parse_block(self, block):
        block = w3.eth.get_block(block)
        wallets = await self._repository.get_wallets()
        self.hash_trans = await self._repository.get_trans_by_status("PENDING")
        parse_data = []
        iterator = self.forward_iterator(block.transactions)
        await broker.publish(message={'m': f'hi {block.number}'}, queue='parser/hash')
        async for transaction_block in iterator:
            _hash = hexbytes.HexBytes(transaction_block).hex()
            if _hash in self.hash_trans:
                print(f"hash - {_hash}")
                transaction = w3.eth.get_transaction(_hash)
                transaction_receipt = w3.eth.get_transaction_receipt(_hash)
                hash_data = await parse_trans_data(transaction, block.timestamp, transaction_receipt.get('status'), _hash)
                update_trans = await self._repository.update_trans(hash_data)
                self.hash_trans.append(_hash)
                # await self.update_wallet_balance(transaction.get('from'), transaction.get('to'), wallets)
                parse_data.append(update_trans)
            else:
                transaction = w3.eth.get_transaction(_hash)
                if transaction.get('from') in wallets or transaction.get('to') in wallets:
                        print(f"from - {transaction.get('from')}")
                        print(f"to - {transaction.get('to')}")
                        transaction_receipt = w3.eth.get_transaction_receipt(_hash)
                        hash_data = await parse_trans_data(transaction, block.timestamp, transaction_receipt.get('status'), _hash)
                        new_trans = await self._repository.add_trans(hash_data)
                        self.hash_trans.append(_hash)
                        # await self.update_wallet_balance(transaction.get('from'), transaction.get('to'), wallets)
                        parse_data.append(new_trans)
        print('---DONE---')
        return parse_data

    async def update_wallet_balance(self, from_address, to_address, wallets):
        if from_address in wallets:
            balance_wei = w3.eth.get_balance(from_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            await self._repository.update_balance(from_address, balance_eth)

        if to_address in wallets:
            balance_wei = w3.eth.get_balance(to_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            await self._repository.update_balance(to_address, balance_eth)


    async def get_hash_data(self, _hash):
        url = f'https://deep-index.moralis.io/api/v2/transaction/{_hash}?chain=sepolia'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                trans = response.json()
                return trans
            else:
                return False


