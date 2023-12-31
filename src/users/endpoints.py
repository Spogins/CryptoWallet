from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.users.containers import Container
from src.users.repository import NotFoundError
from src.users.schemas import UserModel, UserProfile
from src.users.services.user import UserService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


@app.get("/users", status_code=status.HTTP_200_OK)
@inject
async def get_all(user_service: UserService = Depends(Provide[Container.user_service]),
                  bearer: HTTPAuthorizationCredentials = Depends(user_auth)
                  ):
    return await user_service.get_users()


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
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
    user = await get_user_from_bearer(bearer)
    return await user_service.edit_profile(profile, user)


@app.get("/user_auth", status_code=status.HTTP_200_OK)
@inject
async def user_auth(
        user_service: UserService = Depends(Provide[Container.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    user_id = await get_user_from_bearer(bearer)
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
