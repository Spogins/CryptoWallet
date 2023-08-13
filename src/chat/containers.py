from dependency_injector import containers, providers
from src.core.containers import Container as db_container
from src.chat.repository import ChatRepository
from src.chat.services.chat import ChatService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat'
    ]
    )
    chat_repository = providers.Factory(ChatRepository, session_factory=db_container.session)
    chat_service = providers.Factory(ChatService, chat_repository=chat_repository)