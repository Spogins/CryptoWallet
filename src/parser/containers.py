
from dependency_injector import containers, providers
from src.core.containers import Container as db_container
from src.parser.services.block_parser import ParserService
from src.wallet.repository import WalletRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat'
    ]
    )
    wallet_repository = providers.Factory(WalletRepository, session_factory=db_container.session)
    parser_service = providers.Factory(ParserService, wallet_repository=wallet_repository)
