from web3 import Web3, HTTPProvider

DEBUG = True

# DATABASE
DB_NAME = 'crypto_wallet'
DB_USER = 'admin_user'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = 5432

URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

JWT_SECRET = 'crypto_wallet'
ALGORITHM = 'HS256'

MAIL_USERNAME = 'spogins@gmail.com'
MAIL_PASSWORD = "uivqpoilnvnxgkba"
MAIL_FROM = 'spogins@gmail.com'
MAIL_PORT = 587
MAIL_SERVER = 'smtp.gmail.com'
MAIL_FROM_NAME = 'CryptoWallet'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

QUICKNODE_URL = 'https://damp-cosmopolitan-sea.ethereum-sepolia.discover.quiknode.pro/f9b662c08002faf65b111387307c448466c1ecc0/'

MORALIS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjkxOGEwY2JmLTkxNjctNDgxZS1iYTRkLWFkNjRjNWVkZTg2MyIsIm9yZ0lkIjoiMzUyMzI0IiwidXNlcklkIjoiMzYyMTI4IiwidHlwZSI6IlBST0pFQ1QiLCJ0eXBlSWQiOiJlNjJkOWI2Yy01MTRjLTQ2MDMtOGJlYi1kZDk3MGM0NzU5NzAiLCJpYXQiOjE2OTE2MDE1OTAsImV4cCI6NDg0NzM2MTU5MH0.Ww5foE2uKxgr8FCLGIgRQQ8wvazz-5UJ3Yag3m0QxHM'

w3 = Web3(HTTPProvider(QUICKNODE_URL))

ALLOWED_HOSTS = ['http://127.0.0.1:8000']
