import time
from asgiref.sync import async_to_sync, sync_to_async
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config.settings import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_SERVER, MAIL_FROM_NAME
from config_celery.celery import celery


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


celery.conf.beat_schedule = {
    "send-mail": {
        "task": ["src.celery.auth_tasks.send_mail"],
        "schedule": 30.0  # Every 30 seconds, adjust as needed
    },
    "chat-access": {
        "task": ["src.celery.auth_tasks.chat_access"],
        "schedule": 30.0  # Every 30 seconds, adjust as needed
    }
}


@celery.task
def send_mail(email):
    print('send_mail')
    html = """<p>Hi you have successfully registered on Crypto Wallet!</p> """

    message = MessageSchema(
        subject="Register success!",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    async_to_sync(fm.send_message)(message, template_name=html)




# @celery.task
# def chat_access_task(user):
#     print('chat_access_task')
#     time.sleep(20)



