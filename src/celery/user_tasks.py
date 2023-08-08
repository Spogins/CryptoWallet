# from config_celery.celery import celery
#
#
# celery.conf.beat_schedule = {
#     "send-mail": {
#         "task": ["src.celery.user_tasks.chat_access"],
#         "schedule": 30.0  # Every 30 seconds, adjust as needed
#     }
# }
#
#
# @celery.task
# def chat_access():
#     print('chat_access')
