import asyncio
from dependency_injector.wiring import Provide, inject
from config_celery.celery import celery
from src.auth.services.auth import AuthService
from src.auth.containers import Container


@celery.task
@inject
def chat_access(user_id, auth_service: AuthService = Provide[Container.auth_service]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auth_service.chat_access(user_id))
