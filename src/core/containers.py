from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG, URL, DATABASE_TEST_URL
from src.core.db import Database


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    db = providers.Singleton(Database, db_url=URL)
    session = providers.Callable(db.provided.session)


# @containers.override(Container)
# class OverridingContainer(containers.DeclarativeContainer):
#     wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
#     db = providers.Singleton(Database, db_url=DATABASE_TEST_URL)
#     session = providers.Callable(db.provided.session)
#
#
# class TestContainer(containers.DeclarativeContainer):
#
#     wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
#     db = providers.Singleton(Database, db_url=DATABASE_TEST_URL)
#     session = providers.Callable(db.provided.session)
#
#


