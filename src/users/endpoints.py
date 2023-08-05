from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status, Request
import jwt
from config.settings import JWT_SECRET, ALGORITHM
from src.users.containers import Container
from src.users.repository import NotFoundError
from src.users.schemas import UserModel,UserProfile
from src.users.services.user import UserService

app = APIRouter()


@app.get("/users")
@inject
async def get_all(user_service: UserService = Depends(Provide[Container.user_service])):
    return await user_service.get_users()


@app.get("/user/{user_id}")
@inject
async def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/user", status_code=status.HTTP_201_CREATED)
@inject
async def add(user: UserModel,
              user_service: UserService = Depends(Provide[Container.user_service]),
              ):
    return await user_service.create_user(user)


@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
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
                       request: Request,
                       user_service: UserService = Depends(Provide[Container.user_service]),
                       ):
    try:
        token = request.cookies.get('access_token')
        verify = jwt.decode(token, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
        email = verify.get('user_email')
        return await user_service.edit_profile(profile, email)
    except:
        return {'access_token': 'expire token'}

