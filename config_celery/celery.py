import time
from celery import Celery
from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,  # Update with your Redis URL
    backend=CELERY_RESULT_BACKEND,# Update with your Redis URL
    include=["src.celery.auth_tasks", "src.celery.user_tasks", "config_celery.celery"]
)


celery.conf.beat_schedule = {
    "test-task": {
        "task": "config_celery.celery.test_task",  # Используйте строку, не список
        "schedule": 30.0  # Every 30 seconds, adjust as needed
    }
}


@celery.task
def test_task():
    time.sleep(10)
    print('-test task-')