import datetime
import json
import time
from typing import Callable

from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from config.settings import JWT_SECRET, ALGORITHM
from src.auth.schemas import RegisterUserModel, UserForm
import jwt

from src.users.models import User


class AuthRepository:

    def __init__(self, session_factory: Callable[..., Session]) -> None:
        self.session_factory = session_factory

    async def token(self, user):
        with self.session_factory() as session:
            _user = session.query(User).filter(User.email == user.email).first()
            if pbkdf2_sha256.verify(user.password, _user.password):
                payload = {"id": _user.id,
                           'created': datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
                if not user.remember:
                    expiration_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=15)
                    payload["exp"] = expiration_time

                token = jwt.encode(
                    payload,
                    JWT_SECRET,
                    algorithm=ALGORITHM
                )
                return token
            else:
                raise HTTPException(status_code=401, detail="Wrong email address or password")

    async def add(self, user_model: RegisterUserModel) -> User:
        with self.session_factory() as session:
            user = User(email=user_model.email, password=user_model.password, username=user_model.username)
            session.add(user)
            session.commit()
            session.refresh(user)

            from src.celery.auth_tasks import send_mail, chat_access_task
            send_mail.apply_async(args=(user.email,))
            chat_access_task(user.id)
            return UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar)

    def chat_access(self, user):
        with self.session_factory() as session:
            _user = session.query(User).filter(User.id == user).first()
            _user.chat_access = True
            session.commit()
            session.refresh(_user)




