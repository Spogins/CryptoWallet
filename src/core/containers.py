from dependency_injector import containers, providers

from src.core.db import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth', 'src.wallet.services',
        'src.wallet', 'src.parser.services', 'src.parser', 'config_socketio', 'src.chat.services',
        'src.chat'
    ])
    db = providers.Singleton(Database)
    session = providers.Callable(db.provided.session)
