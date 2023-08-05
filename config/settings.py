#DATABASE
DB_NAME = 'crypto_wallet'
DB_USER = 'admin_user'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = 5432

URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

JWT_SECRET = 'crypto_wallet'
ALGORITHM = 'HS256'
