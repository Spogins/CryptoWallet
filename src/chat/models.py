from sqladmin import ModelView
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from src.core.db import Base


class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    image = Column(URLType, nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])


class ChatMessageAdmin(ModelView, model=ChatMessage):
    column_list = [
        ChatMessage.id,
        ChatMessage.text,
        ChatMessage.image,
        ChatMessage.date,
        ChatMessage.user_id,
        ChatMessage.user
    ]