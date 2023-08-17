import hexbytes
from propan import RabbitBroker
from config.settings import w3, RABBITMQ_URL
from src.parser.repository import ParserRepository
from src.web3.w3_service import WebService


class ParserService:
    block = None

    def __init__(self, parser_repository: ParserRepository, w3_service: WebService) -> None:
        self._repository: ParserRepository = parser_repository
        self.w3_service: WebService = w3_service

    @staticmethod
    async def forward_iterator(lst):
        for item in lst:
            yield item

    async def get_block(self):
        latest_block = await self.w3_service.get_block()
        if self.block is None or latest_block > self.block:
            print('---FIND_BLOCK---')
            self.block = latest_block
            async with RabbitBroker(RABBITMQ_URL) as broker:
                await broker.publish(message=self.block, queue='parser/parse_block')
            return self.block

    async def parse_block(self, block):
        block = w3.eth.get_block(block)
        wallets = await self._repository.get_wallets()
        self.hash_trans = await self._repository.get_trans_by_status("PENDING")
        iterator = self.forward_iterator(block.transactions)
        async for transaction_block in iterator:
            _hash = hexbytes.HexBytes(transaction_block).hex()
            if _hash in self.hash_trans:
                print(f"hash - {_hash}")
                async with RabbitBroker(RABBITMQ_URL) as broker:
                    await broker.publish(message={'update': _hash}, queue='wallet/hash')
                self.hash_trans.append(_hash)
            else:
                transaction = w3.eth.get_transaction(_hash)
                if transaction.get('from') in wallets or transaction.get('to') in wallets:
                    print(f"from - {transaction.get('from')}")
                    print(f"to - {transaction.get('to')}")
                    async with RabbitBroker(RABBITMQ_URL) as broker:
                        await broker.publish(message={'create': _hash}, queue='wallet/hash')
                    self.hash_trans.append(_hash)
        print('---DONE---')























    # # async def get_block(self):
    # #     self.block = await self._repository.get_block()
    # #     block_latest = w3.eth.get_block('latest')
    # #     block = w3.eth.get_block(self.block)
    # #     if not block_latest == block:
    # #         await self._repository.update_block(block_latest.number)
    # #         print('---FIND_BLOCK---')
    # #         print(f"---{block.number}---")
    # #         return await self.parse_block(block)
    # #     else:
    # #         print('---SKIP_BLOCK---')
    #
    # async def parse_block(self, block):
    #     block = w3.eth.get_block(block)
    #     wallets = await self._repository.get_wallets()
    #     self.hash_trans = await self._repository.get_trans_by_status("PENDING")
    #     # parse_data = []
    #     iterator = self.forward_iterator(block.transactions)
    #     async with RabbitBroker(RABBITMQ_URL) as broker:
    #         await broker.publish(message={'update': 'HASj'}, queue='wallet/hash')
    #     async for transaction_block in iterator:
    #         _hash = hexbytes.HexBytes(transaction_block).hex()
    #         if _hash in self.hash_trans:
    #             print(f"hash - {_hash}")
    #             async with RabbitBroker(RABBITMQ_URL) as broker:
    #                 await broker.publish(message={'update': _hash}, queue='wallet/hash')
    #             # transaction = w3.eth.get_transaction(_hash)
    #             # transaction_receipt = w3.eth.get_transaction_receipt(_hash)
    #             # hash_data = await parse_trans_data(transaction, block.timestamp, transaction_receipt.get('status'), _hash)
    #             # update_trans = await self._repository.update_trans(hash_data)
    #             self.hash_trans.append(_hash)
    #             # await self.update_wallet_balance(transaction.get('from'), transaction.get('to'), wallets)
    #             # parse_data.append(update_trans)
    #         else:
    #             transaction = w3.eth.get_transaction(_hash)
    #             if transaction.get('from') in wallets or transaction.get('to') in wallets:
    #                     print(f"from - {transaction.get('from')}")
    #                     print(f"to - {transaction.get('to')}")
    #                     async with RabbitBroker(RABBITMQ_URL) as broker:
    #                         await broker.publish(message={'create': _hash}, queue='wallet/hash')
    #                     # transaction_receipt = w3.eth.get_transaction_receipt(_hash)
    #                     # hash_data = await parse_trans_data(transaction, block.timestamp, transaction_receipt.get('status'), _hash)
    #                     # new_trans = await self._repository.add_trans(hash_data)
    #                     self.hash_trans.append(_hash)
    #                     # await self.update_wallet_balance(transaction.get('from'), transaction.get('to'), wallets)
    #                     # parse_data.append(new_trans)
    #     print('---DONE---')


    # async def update_wallet_balance(self, from_address, to_address, wallets):
    #     if from_address in wallets:
    #         balance_wei = w3.eth.get_balance(from_address)
    #         balance_eth = w3.from_wei(balance_wei, 'ether')
    #         await self._repository.update_balance(from_address, balance_eth)
    #
    #     if to_address in wallets:
    #         balance_wei = w3.eth.get_balance(to_address)
    #         balance_eth = w3.from_wei(balance_wei, 'ether')
    #         await self._repository.update_balance(to_address, balance_eth)


    # async def get_hash_data(self, _hash):
    #     url = f'https://deep-index.moralis.io/api/v2/transaction/{_hash}?chain=sepolia'
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(url, headers=self.headers)
    #         if response.status_code == 200:
    #             trans = response.json()
    #             return trans
    #         else:
    #             return False


