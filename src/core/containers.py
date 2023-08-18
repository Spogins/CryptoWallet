from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.core.db import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    db = providers.Singleton(Database)
    session = providers.Callable(db.provided.session)
