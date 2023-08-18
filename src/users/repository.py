from typing import Callable, Iterator, List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models import User
from src.users.schemas import UserModel, UserForm, UserProfile


class UserRepository:

    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> list[UserForm]:
        async with self.session_factory() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return [UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar) for user in users]

    async def get_by_id(self, user_id: int) -> UserForm:
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=401, detail=f"User not found, id: {user_id}")
            return UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar)

    async def add(self, user_model: UserModel) -> User:
        async with self.session_factory() as session:
            user = User(email=user_model.email, password=user_model.password, username=user_model.username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def delete_by_id(self, user_id: int) -> None:
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=401, detail=f"User not found, id: {user_id}")
            await session.delete(user)
            await session.commit()

    async def edit_profile(self, profile: UserProfile, user, psw):
        async with self.session_factory() as session:
            user = await session.get(User, user)
            if user:
                if psw == '' and profile.username == '' and profile.avatar == '':
                    return {'message': 'No changes.'}

                if not psw == '':
                    user.password = psw

                if not profile.username == '':
                    user.username = profile.username

                if not profile.avatar == '':
                    user.avatar = profile.avatar

                await session.commit()
                await session.refresh(user)
                return UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar)
            else:
                return {'error': 'something goes wrong'}


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"