from celery import Celery
from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,  # Update with your Redis URL
    backend=CELERY_RESULT_BACKEND,# Update with your Redis URL
    include=[
        "src.celery.auth_tasks",
        "src.celery.user_tasks",
        "config_celery.celery",
        'src.celery.parse_tasks',
        'src.celery.chat_access_tasks',
        'src.celery.wallet_tasks'

    ]
)

celery.conf.beat_schedule = {
    "parsing": {
        "task": "src.celery.parse_tasks.parsing",
        "schedule": 5.0  # Every 30 seconds, adjust as needed
    },
}
