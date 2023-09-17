from sqladmin import ModelView
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from src.core.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    avatar = Column(URLType, nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    chat_access = Column(Boolean, default=False)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.username,
        User.password,
        User.created_on,
        User.avatar,
        User.is_superuser,
        User.is_active,
        User.chat_access
    ]




