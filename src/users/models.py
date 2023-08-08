from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from src.core.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    avatar = Column(String, default='str')
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    chat_access = Column(Boolean, default=False)
