from asgiref.sync import async_to_sync
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


@celery.task
def send_mail(email: str = 'user@user.com'):
    print('send_mail')
    html = """<p>Hi you have successfully registered on Crypto Wallet!</p> """

    message = MessageSchema(
        subject="Register success!",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    async_to_sync(fm.send_message)(message, template_name=html)



