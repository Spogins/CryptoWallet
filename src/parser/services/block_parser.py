import hexbytes
from propan import RabbitBroker
from config.settings import RABBITMQ_URL
from src.parser.repository import ParserRepository
from src.web3.w3_service import WebService


class ParserService:

    def __init__(self, parser_repository: ParserRepository, w3_service: WebService) -> None:
        self._repository: ParserRepository = parser_repository
        self.w3_service: WebService = w3_service

    @staticmethod
    async def forward_iterator(lst):
        for item in lst:
            yield item

    async def parse_block(self, block):
        block = await self.w3_service.get_block(block)
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
                transaction = await self.w3_service.get_trans(_hash)
                if transaction.get('from') in wallets or transaction.get('to') in wallets:
                    print(f"from - {transaction.get('from')}")
                    print(f"to - {transaction.get('to')}")
                    async with RabbitBroker(RABBITMQ_URL) as broker:
                        await broker.publish(message={'create': _hash}, queue='wallet/hash')
                    self.hash_trans.append(_hash)
        print('---DONE---')
