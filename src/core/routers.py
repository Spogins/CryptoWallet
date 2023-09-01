from fastapi import APIRouter
from src.users.endpoints import app as user_app
from src.auth.endpoints import app as auth_app
from src.delivery.endpoints import app as delivery_app
from src.wallet.endpoints import app as wallet_app
from src.chat.endpoints import app as chat_app
from src.ibay.endpoints import app as ibay_app


router_app = APIRouter()
API_PREFIX = "/api/v1"

router_app.include_router(ibay_app, prefix=API_PREFIX, tags=["iBay"])
router_app.include_router(delivery_app, prefix=API_PREFIX, tags=["Delivery"])
router_app.include_router(wallet_app, prefix=API_PREFIX, tags=["Wallets"])
router_app.include_router(auth_app, prefix=API_PREFIX, tags=["Auth"])
router_app.include_router(user_app, prefix=API_PREFIX, tags=["User"])
router_app.include_router(chat_app, prefix=API_PREFIX, tags=["Chat"])