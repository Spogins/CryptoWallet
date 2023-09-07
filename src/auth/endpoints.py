import datetime
import json
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Cookie
from fastapi.security import HTTPAuthorizationCredentials
from config_fastapi.fastapi_mgr import fastapi_mgr, templates
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.schemas import AuthUsers, RegisterUserModel
from src.auth.services.auth import AuthService
from src.celery.chat_access_tasks import chat_access


app = APIRouter()

user_auth = AutoModernJWTAuth()
mgr = fastapi_mgr


@app.post("/log_in", status_code=status.HTTP_200_OK)
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



@app.post("/log_out", status_code=status.HTTP_200_OK)
@inject
async def log_out(bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    response = Response(content='{"message": "Logged out successfully"}')
    response.set_cookie("access_token", value="", max_age=0)
    return response


@app.post("/registration", status_code=status.HTTP_201_CREATED)
@inject
async def registration(user: RegisterUserModel, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    user = await auth_service.register_user(user)
    if user.id:
        chat_access.apply_async(args=[user.id], countdown=60)
    return user
