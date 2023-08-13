from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.chat.containers import Container
from src.chat.schemas import MessageForm
from src.chat.services.chat import ChatService
from utils.base.get_user_bearer import get_user_from_bearer

app = APIRouter()

user_auth = AutoModernJWTAuth()


@app.get("/test")
@inject
async def log_out(chat_service: ChatService = Depends(Provide[Container.chat_service]),
                  bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    return {'m': 'test'}


@app.post("/send_message")
@inject
async def send_message(message: MessageForm, chat_service: ChatService = Depends(Provide[Container.chat_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.send_message(message, user_id)


@app.get("/get_chat")
@inject
async def get_chat(limit: int = 10, chat_service: ChatService = Depends(Provide[Container.chat_service])):
    return await chat_service.get_chat(limit)
