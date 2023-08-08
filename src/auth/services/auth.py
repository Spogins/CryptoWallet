from typing import Callable
from src.auth.repository import AuthRepository


class AuthService:

    def __init__(self, auth_repository: AuthRepository, hashed_psw: Callable[[str], str]) -> None:
        self._repository: AuthRepository = auth_repository
        self.hashed_psw = hashed_psw

    async def token(self, user):
        return await self._repository.token(user)

    async def register_user(self, user):
        user_model = user
        hashed_psw = self.hashed_psw(user.password)
        user_model.password = hashed_psw
        return await self._repository.add(user_model)

    def chat_access(self, user):
        return self._repository.chat_access(user)






