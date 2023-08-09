import passlib.hash
from dependency_injector import containers, providers
from src.auth.repository import AuthRepository
from src.auth.services.auth import AuthService
from src.core.containers import Container as db_container


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet'
        ]
    )
    auth_repository = providers.Factory(AuthRepository, session_factory=db_container.session)
    password_hasher = providers.Callable(passlib.hash.pbkdf2_sha256.hash)
    auth_service = providers.Factory(AuthService, auth_repository=auth_repository, hashed_psw=password_hasher.provider)