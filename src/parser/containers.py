from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.core.containers import Container as db_container
from src.parser.repository import ParserRepository
from src.parser.services.block_parser import ParserService
from src.web3.w3_service import WebService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    parser_repository = providers.Factory(ParserRepository, session_factory=db_container.session)
    w3_service = providers.Factory(WebService)
    parser_service = providers.Factory(ParserService, parser_repository=parser_repository, w3_service=w3_service)
