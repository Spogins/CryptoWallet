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
        hash_trans = await self._repository.get_trans_by_status("PENDING")
        parsed_hash = []
        iterator = self.forward_iterator(block.transactions)
        async for transaction_block in iterator:
            _hash = hexbytes.HexBytes(transaction_block).hex()
            if _hash in parsed_hash:
                continue

            if _hash in hash_trans:
                await self.send_hash({'update': _hash})
                parsed_hash.append(_hash)
            else:
                transaction = await self.w3_service.get_trans(_hash)
                if transaction.get('from') in wallets or transaction.get('to') in wallets:
                    await self.send_hash({'create': _hash})
                    parsed_hash.append(_hash)

        print('---DONE---')

    @staticmethod
    async def send_hash(data):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='wallet/hash')
