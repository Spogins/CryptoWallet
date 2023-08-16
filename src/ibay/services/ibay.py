from src.ibay.repository import IBayRepository


class IBayService:

    def __init__(self, ibay_repository: IBayRepository) -> None:
        self._repository: IBayRepository = ibay_repository

    async def test(self):
        print('test')
        return {'mn': 'test'}

    async def add_product(self, product):
        return await self._repository.add(product)

    async def get_products(self):
        return await self._repository.get_all()

    async def get_product(self, pr_id):
        return await self._repository.get(pr_id)

    async def update_product(self, _product):
        return await self._repository.update(_product)

    async def remove_product(self, pr_id):
        return await self._repository.remove_pr(pr_id)