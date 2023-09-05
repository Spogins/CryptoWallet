import jwt
from config.settings import JWT_SECRET, ALGORITHM


async def get_user_from_bearer(bearer):
    token = bearer.credentials
    verify = jwt.decode(token, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
    user_id = verify.get('id')
    return user_id

