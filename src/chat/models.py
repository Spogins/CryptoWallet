from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from sqlalchemy_utils import URLType
from src.core.db import Base


class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    image = Column(URLType, nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))


