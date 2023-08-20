from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.core.containers import Container as db_container
from src.delivery.repository import DeliveryRepository
from src.delivery.services.delivery import DeliveryService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    delivery_repository = providers.Factory(DeliveryRepository, session_factory=db_container.session)
    delivery_service = providers.Factory(DeliveryService, delivery_repository=delivery_repository)
