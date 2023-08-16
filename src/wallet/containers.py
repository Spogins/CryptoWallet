from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.core.containers import Container as db_container
from src.wallet.repository import WalletRepository
from src.wallet.services.wallet import WalletService
from src.web3.w3_service import WebService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    wallet_repository = providers.Factory(WalletRepository, session_factory=db_container.session)
    w3_service = providers.Factory(WebService)
    wallet_service = providers.Factory(WalletService, wallet_repository=wallet_repository, w3_service=w3_service)
