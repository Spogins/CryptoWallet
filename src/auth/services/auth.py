import json
from typing import Callable

import jwt
from starlette.responses import RedirectResponse
from fastapi import Response
from config.settings import JWT_SECRET, ALGORITHM
from src.auth.repository import AuthRepository
from utils.base.get_user_bearer import get_user_from_bearer


class AuthService:

    def __init__(self, auth_repository: AuthRepository, hashed_psw: Callable[[str], str]) -> None:
        self._repository: AuthRepository = auth_repository
        self.hashed_psw = hashed_psw

    async def get_auth(self, request):
        if request.cookies.get('access_token'):
            jwt_string = request.cookies.get('access_token')
            jwt_token = jwt_string.split(" ")[1]
            verify = jwt.decode(jwt_token, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
            if verify.get('id'):
                return True
        return False

    async def token(self, user):
        return await self._repository.token(user)

    async def admin_token(self, username, password):
        token = await self._repository.admin_token(username, password)
        if token:
            data = {'access_token': token}
            content = json.dumps(data)
            response = Response(content=content)
            response.set_cookie(key="access_token", value=f'Bearer {content}', max_age=1735707600)
            return True
        return False


    async def register_user(self, user):
        user_model = user
        hashed_psw = self.hashed_psw(user.password)
        user_model.password = hashed_psw
        return await self._repository.add(user_model)

    async def chat_access(self, user_id):
        return await self._repository.get_access(user_id)










