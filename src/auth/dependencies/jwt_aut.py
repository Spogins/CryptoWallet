import jwt
from dependency_injector.wiring import inject
from fastapi import Request
from config.settings import JWT_SECRET, ALGORITHM
from utils.security.base import JwtHTTPBearer


class AutoModernJWTAuth(JwtHTTPBearer):

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @inject
    async def __call__(self, request: Request):
        bearer = await super().__call__(request)
        if await token_verify(bearer.credentials):
            return bearer
        return None


async def token_verify(bearer):
    verify = jwt.decode(bearer, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
    return verify

