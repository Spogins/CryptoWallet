from fastapi import HTTPException
from src.boto3.boto3_service import BotoService
from src.chat.repository import ChatRepository
from src.chat.schemas import MessageForm


class ChatService:

    def __init__(self, chat_repository: ChatRepository, boto3_service: BotoService) -> None:
        self._repository: ChatRepository = chat_repository
        self.boto3_service: BotoService = boto3_service

    async def send_message(self, message: MessageForm, user_id):
        if message.text == '' and message.image == '':
            raise HTTPException(status_code=401,
                                detail='Message empty data.')
        elif not message.image == '':
            message.image = await self.boto3_service.upload_image(message.image)

        return await self._repository.add(message, user_id)

    async def get_chat(self, limit):
        return await self._repository.get_chat_messages(limit)

