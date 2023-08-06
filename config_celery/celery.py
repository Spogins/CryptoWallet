from celery import shared_task, Celery

from config import settings
from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,  # Update with your Redis URL
    backend=CELERY_RESULT_BACKEND,  # Update with your Redis URL
    include=["src.auth.t_task"]
)

celery.conf.beat_schedule = {
    "test-task": {
        "task": "src.auth.t_task.test_task",
        "schedule": 30.0  # Every 30 seconds, adjust as needed
    }
}
