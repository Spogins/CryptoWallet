from fastapi import HTTPException

from src.chat.repository import ChatRepository
from src.chat.schemas import MessageForm


class ChatService:

    def __init__(self, chat_repository: ChatRepository) -> None:
        self._repository: ChatRepository = chat_repository

    async def send_message(self, message: MessageForm, user_id):
        if message.text == '' and message.image == '':
            raise HTTPException(status_code=401,
                                detail='Message empty data.')
        else:
            return await self._repository.add(message, user_id)

    async def get_chat(self, limit):
        return await self._repository.get_chat_messages(limit)

