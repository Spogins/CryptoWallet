from propan import RabbitBroker
from config.settings import RABBITMQ_URL
from src.boto3.boto3_service import BotoService
from src.ibay.models import Product
from src.ibay.repository import IBayRepository
from src.ibay.schemas import ProductEdit, BuyProduct


class IBayService:

    def __init__(self, ibay_repository: IBayRepository, boto3_service: BotoService) -> None:
        self._repository: IBayRepository = ibay_repository
        self.boto3_service: BotoService = boto3_service

    async def buy_product(self, product: BuyProduct, user_id):
        product_item: Product = await self._repository.get(product.id)

        from_wallet: str = product.wallet
        data: dict = {
            'from_wallet': from_wallet,
            'to_wallet': product_item.wallet,
            'value': product_item.price,
            'product_id': product_item.id,
            'user_id': user_id
        }
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=data, queue='wallet/buy_product')
        return await self._repository.to_order(product_item.id)

    async def add_product(self, product, user_id):
        if not product.image == '':
            product.image = await self.boto3_service.upload_image(product.image)
        return await self._repository.add(product, user_id)

    async def get_products(self):
        return await self._repository.get_all()

    async def get_product(self, pr_id):
        return await self._repository.get(pr_id)

    async def update_product(self, _product: ProductEdit):
        if not _product.image == '':
            _product.image = await self.boto3_service.upload_image(_product.image)
        return await self._repository.update(_product)
