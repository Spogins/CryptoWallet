from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.web3.repository import WebRepository
from src.web3.w3_service import WebService
from src.core.containers import Container as db_container


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    web3_repository = providers.Factory(WebRepository, session_factory=db_container.session)
    web3_service = providers.Singleton(WebService, web3_repository=web3_repository)
