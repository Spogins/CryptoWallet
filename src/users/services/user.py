from typing import Iterator, Callable
from src.users.models import User
from src.users.repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository, hashed_psw: Callable[[str], str]) -> None:
        self._repository: UserRepository = user_repository
        self.hashed_psw = hashed_psw

    async def get_users(self) -> Iterator[User]:
        return await self._repository.get_all()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self._repository.get_by_id(user_id)

    async def create_user(self, user) -> User:
        user_model = user
        hashed_psw = self.hashed_psw(user.password)
        user_model.password = hashed_psw
        return await self._repository.add(user_model)

    async def delete_user_by_id(self, user_id: int) -> None:
        return await self._repository.delete_by_id(user_id)

    async def edit_profile(self, profile, user):
        psw = profile.new_password
        if not profile.new_password == '':
            psw = self.hashed_psw(psw)
        return await self._repository.edit_profile(profile, user, psw)
