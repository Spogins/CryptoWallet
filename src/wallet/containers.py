from dependency_injector import containers, providers
from src.core.containers import Container as db_container
from src.wallet.repository import WalletRepository
from src.wallet.services.wallet import WalletService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat', 'src',
    ]
    )
    wallet_repository = providers.Factory(WalletRepository, session_factory=db_container.session)
    wallet_service = providers.Factory(WalletService, wallet_repository=wallet_repository)
