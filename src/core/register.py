from dependency_injector import containers, providers
from src.auth.containers import Container as AuthContainer
from src.core.containers import Container as DatabaseContainer
from src.users.containers import Container as UserContainer
from src.wallet.containers import Container as WalletContainer
from src.parser.containers import Container as ParserContainer
from src.chat.containers import Container as ChatContainer
from src.ibay.containers import Container as IBayContainer



class RegisterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat', 'src',
    ]
    )
    users_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
    db_container = providers.Container(DatabaseContainer)
    wallet_container = providers.Container(WalletContainer)
    parser_container = providers.Container(ParserContainer)
    chat_container = providers.Container(ChatContainer)
    ibay_container = providers.Container(IBayContainer)