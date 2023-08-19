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

    async def parse_block(self, block) -> None:
        block = await self.w3_service.get_block(block)
        parsed_hash = []
        iterator = self.forward_iterator(block.transactions)
        async for transaction_hash in iterator:
            _hash = hexbytes.HexBytes(transaction_hash).hex()
            if _hash in parsed_hash:
                continue
            if await self._repository.get_db_trans(_hash):
                await self.send_hash({'update': _hash})
                parsed_hash.append(_hash)
            else:
                transaction = await self.w3_service.get_trans(_hash)
                if await self._repository.get_wallet(transaction.get('from')) or await self._repository.get_wallet(transaction.get('to')):
                    await self.send_hash({'create': _hash})
                    parsed_hash.append(_hash)
        print('---DONE---')

    @staticmethod
    async def send_hash(data):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='wallet/hash')
