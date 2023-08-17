from celery import Celery

from config_celery.celery import celery
from src.core.register import RegisterContainer


def create_celery_app() -> Celery:
    container = RegisterContainer()
    celery_app = celery
    return celery_app

celery_app = create_celery_app()