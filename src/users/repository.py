from typing import Callable, Iterator
from sqlalchemy.orm import Session
from src.users.models import User
from src.users.schemas import UserModel, UserForm, UserProfile


class UserRepository:

    def __init__(self, session_factory: Callable[..., Session]) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            users = session.query(User).all()
            return [UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar) for user in users]

    async def get_by_id(self, user_id: int) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar)

    async def add(self, user_model: UserModel) -> User:
        with self.session_factory() as session:
            user = User(email=user_model.email, password=user_model.password, username=user_model.username)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    async def delete_by_id(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit()

    async def edit_profile(self, profile: UserProfile, user, psw):
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user).first()
            if user:
                if not psw == '':
                    user.password = psw
                user.username = profile.username
                session.commit()
                session.refresh(user)
                return UserForm(id=user.id, email=user.email, username=user.username, avatar=user.avatar)
            else:
                return {'error': 'something goes wrong'}


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"