import passlib.hash
from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.core.containers import Container as db_container
from src.users.repository import UserRepository
from src.users.services.user import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    user_repository = providers.Factory(UserRepository, session_factory=db_container.session)
    password_hasher = providers.Callable(passlib.hash.pbkdf2_sha256.hash)
    user_service = providers.Factory(UserService, user_repository=user_repository, hashed_psw=password_hasher.provider)
