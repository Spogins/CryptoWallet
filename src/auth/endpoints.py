import datetime
import json
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Cookie
import jwt
from fastapi.security import HTTPAuthorizationCredentials
from config.settings import JWT_SECRET, ALGORITHM
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.schemas import AuthUsers, RegisterUserModel
from src.auth.services.auth import AuthService


app = APIRouter()

user_auth = AutoModernJWTAuth()

@app.post("/log_in")
@inject
async def get_token(user: AuthUsers, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    token = await auth_service.token(user)
    data = {'access_token': token}
    content = json.dumps(data)
    response = Response(content=content)
    if not user.remember:
        expire_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=15)
        response.set_cookie(key="access_token", value=f'Bearer {token}',
                            expires=expire_time.strftime('%a, %d-%b-%Y %T GMT'))
    else:
        response.set_cookie(key="access_token", value=f'Bearer {token}', max_age=1735707600)
    return response


@app.post("/log_out")
@inject
async def log_out(bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    response = Response(content='{"message": "Logged out successfully"}')
    response.set_cookie("access_token", value="", max_age=0)
    return response


@app.get("/token_user")
@inject
async def token_user(access_token: str = Cookie(None)):
    return access_token


@app.get("/verify_token")
@inject
async def verify_token(access_token: str = Cookie(None)):
    try:
        verify = jwt.decode(access_token, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
        return {'access_token': verify}
    except:
        return {'access_token': 'expire token'}


@app.post("/registration", status_code=status.HTTP_201_CREATED)
@inject
async def registration(user: RegisterUserModel, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    return await auth_service.register_user(user)
