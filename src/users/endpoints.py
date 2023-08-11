import httpx as httpx
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Request
import jwt
from fastapi.security import HTTPAuthorizationCredentials
from config.settings import JWT_SECRET, ALGORITHM
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.users.containers import Container
from src.users.repository import NotFoundError
from src.users.schemas import UserModel, UserProfile
from src.users.services.user import UserService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


@app.get("/users")
@inject
async def get_all(user_service: UserService = Depends(Provide[Container.user_service]),
                  bearer: HTTPAuthorizationCredentials = Depends(user_auth)
                  ):
    return await user_service.get_users()


@app.get("/user/{user_id}")
@inject
async def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/user", status_code=status.HTTP_201_CREATED)
@inject
async def add(user: UserModel,
              user_service: UserService = Depends(Provide[Container.user_service]),
              bearer: HTTPAuthorizationCredentials = Depends(user_auth)
              ):
    return await user_service.create_user(user)


@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    try:
        await user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/edit_profile", status_code=status.HTTP_200_OK)
@inject
async def edit_profile(profile: UserProfile,
                       user_service: UserService = Depends(Provide[Container.user_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)
                       ):
    try:
        user = await get_user_from_bearer(bearer)
        return await user_service.edit_profile(profile, user)
    except:
        return {'access_token': 'expire token'}
