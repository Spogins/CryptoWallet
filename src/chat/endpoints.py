from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.chat.containers import Container
from src.chat.schemas import MessageForm, UserList
from src.chat.services.chat import ChatService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


@app.post("/send_message", status_code=status.HTTP_201_CREATED)
@inject
async def send_message(message: MessageForm, chat_service: ChatService = Depends(Provide[Container.chat_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.send_message(message, user_id)


@app.get("/get_chat", status_code=status.HTTP_200_OK)
@inject
async def get_chat(limit: int = 10, chat_service: ChatService = Depends(Provide[Container.chat_service])):
    return await chat_service.get_chat(limit)


@app.get('/user_messages', status_code=status.HTTP_200_OK)
@inject
async def user_messages(chat_service: ChatService = Depends(Provide[Container.chat_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.get_user_messages(user_id)

@app.post('/users_from_chat', status_code=status.HTTP_200_OK)
@inject
async def user_messages(users_list: UserList, chat_service: ChatService = Depends(Provide[Container.chat_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    return await chat_service.get_users(users_list.users)

