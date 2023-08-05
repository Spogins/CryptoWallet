from dependency_injector import containers, providers

from src.core.db import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'src.users', 'src.users.services', 'src.core', 'src.auth.services', 'src.auth'
    ])
    db = providers.Singleton(Database)
    session = providers.Callable(db.provided.session)
