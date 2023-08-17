from src.boto3.boto3_service import BotoService
from src.ibay.repository import IBayRepository
from src.ibay.schemas import ProductEdit


class IBayService:

    def __init__(self, ibay_repository: IBayRepository, boto3_service: BotoService) -> None:
        self._repository: IBayRepository = ibay_repository
        self.boto3_service: BotoService = boto3_service

    async def test(self):
        print('test')
        return {'mn': 'test'}

    async def add_product(self, product):
        if not product.image == '':
            product.image = await self.boto3_service.upload_image(product.image)
        return await self._repository.add(product)

    async def get_products(self):
        return await self._repository.get_all()

    async def get_product(self, pr_id):
        return await self._repository.get(pr_id)

    async def update_product(self, _product: ProductEdit):
        if not _product.image == '':
            _product.image = await self.boto3_service.upload_image(_product.image)
        return await self._repository.update(_product)

    async def remove_product(self, pr_id):
        return await self._repository.remove_pr(pr_id)