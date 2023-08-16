from dependency_injector import containers, providers
from src.core.containers import Container as db_container
from src.ibay.repository import IBayRepository
from src.ibay.services.ibay import IBayService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat', 'src',
    ]
    )
    ibay_repository = providers.Factory(IBayRepository, session_factory=db_container.session)
    ibay_service = providers.Factory(IBayService, ibay_repository=ibay_repository)
