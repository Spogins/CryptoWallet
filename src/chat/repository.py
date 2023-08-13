from collections.abc import Iterator
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.models import ChatMessage
from src.chat.schemas import MessageForm, ChatForm
from src.users.models import User
from utils.base.format_date import convert_date


class ChatRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def add(self, message: MessageForm, user_id: int):
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if message.text == '':
                chat_message = ChatMessage(text='', image=message.image, user=user)
            else:
                chat_message = ChatMessage(text=message.text, user=user)
            session.add(chat_message)
            await session.commit()
            await session.refresh(chat_message)
            return chat_message

    async def get_chat_messages(self, _limit) -> Iterator[ChatMessage]:
        async with self.session_factory() as session:
            stmt = select(ChatMessage).order_by(ChatMessage.id.desc()).limit(_limit)
            result = await session.execute(stmt)
            chat_messages = result.scalars().all()
            return [ChatForm(id=message.id, user_id=message.user_id, text=message.text, image=message.image,
                             date=str(message.date)) for message in chat_messages]
