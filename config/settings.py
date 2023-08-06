DEBUG = True

# DATABASE
DB_NAME = 'crypto_wallet'
DB_USER = 'admin_user'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = 5432

URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

JWT_SECRET = 'crypto_wallet'
ALGORITHM = 'HS256'

MAIL_USERNAME = 'spogins@gmail.com'
MAIL_PASSWORD = "uivqpoilnvnxgkba"
MAIL_FROM = 'spogins@gmail.com'
MAIL_PORT = 587
MAIL_SERVER = 'smtp.gmail.com'
MAIL_FROM_NAME = 'CryptoWallet'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
