from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.web3.w3_service import WebService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    web3_service = providers.Singleton(WebService)