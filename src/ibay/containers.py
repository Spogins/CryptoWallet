from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.boto3.boto3_service import BotoService
from src.core.containers import Container as db_container
from src.ibay.repository import IBayRepository
from src.ibay.services.ibay import IBayService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    ibay_repository = providers.Factory(IBayRepository, session_factory=db_container.session)
    boto3_service = providers.Factory(BotoService)
    ibay_service = providers.Factory(IBayService, ibay_repository=ibay_repository, boto3_service=boto3_service)
