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
        hash_data_list: list = []
        hash_list: list = []
        from_wallet: list = []
        to_wallet: list = []

        iterator = self.forward_iterator(block.transactions)
        async for data in iterator:
            hash_data = await self.w3_service.get_trans(data.hex())
            hash_list.append(hash_data.get('hash').hex())
            from_wallet.append(hash_data.get('from'))
            to_wallet.append(hash_data.get('to'))
            hash_data_list.append(hash_data)

        hash_list: list = await self._repository.get_db_trans(hash_list)
        from_wallet: list = await self._repository.get_wallet(from_wallet)
        to_wallet: list = await self._repository.get_wallet(to_wallet)

        for hash_data in hash_data_list:
            _hash = hash_data.get('hash').hex()
            if _hash in parsed_hash:
                continue
            if _hash in hash_list:
                await self.send_hash({'hash': _hash})
                parsed_hash.append(_hash)
            elif hash_data.get('from') in from_wallet or hash_data.get('to') in to_wallet:
                await self.send_hash({'hash': _hash})
                parsed_hash.append(_hash)

    @staticmethod
    async def send_hash(data):
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='wallet/hash')
