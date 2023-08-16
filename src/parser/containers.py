from dependency_injector import containers, providers
from src.core.containers import Container as db_container
from src.parser.repository import ParserRepository
from src.parser.services.block_parser import ParserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat', 'src',
    ]
    )
    parser_repository = providers.Factory(ParserRepository, session_factory=db_container.session)
    parser_service = providers.Factory(ParserService, parser_repository=parser_repository)