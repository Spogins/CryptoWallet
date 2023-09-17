from collections.abc import Iterator
from datetime import datetime
from typing import Callable, List
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.chat.models import ChatMessage
from src.chat.schemas import MessageForm, ChatForm
from src.users.models import User


class ChatRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory


    async def get_chat_users(self, users):
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.id.in_(users)))
            _users = result.scalars().all()
            return _users


    async def user_messages(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(select(ChatMessage).where(ChatMessage.user_id == user_id))
            res = result.scalars().all()
            return len(res)

    async def add(self, message: MessageForm, user_id: int):
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if user.chat_access:
                if message.text == '':
                    chat_message = ChatMessage(text='', image=message.image, user=user)
                else:
                    chat_message = ChatMessage(text=message.text, user=user, image=message.image)
                session.add(chat_message)
                await session.commit()
                await session.refresh(chat_message)
                return ChatForm(
                    user_id=user.id,
                    text=chat_message.text,
                    image=chat_message.image,
                    date=await self.format_time(chat_message.date),
                    username=user.username,
                    user_avatar=user.avatar
                )
            else:
                raise HTTPException(status_code=401,
                                    detail='User does not have access to the chat')

    async def get_chat_messages(self, _limit) -> list[ChatForm]:
        async with self.session_factory() as session:
            stmt = select(ChatMessage).order_by(ChatMessage.id.desc()).options(joinedload(ChatMessage.user)).limit(
                _limit)
            result = await session.execute(stmt)
            chat_messages = result.scalars().all()

            return [ChatForm(
                user_id=message.user_id,
                text=message.text,
                image=message.image,
                date=await self.format_time(message.date),
                username=message.user.username,
                user_avatar=message.user.avatar
            ) for message in chat_messages]

    @staticmethod
    async def format_time(_date):
        date_obj = datetime.strptime(str(_date), "%Y-%m-%d %H:%M:%S.%f")
        formatted_time = date_obj.strftime("%I:%M %p")
        return formatted_time
