from typing import Annotated
from propan import RabbitBroker
from src.core.register import RegisterContainer
from src.users.endpoints import app as user_app
from src.auth.endpoints import app as auth_app
from src.wallet.endpoints import app as wallet_app
from fastapi import Depends, FastAPI
from propan.fastapi import RabbitRouter

router = RabbitRouter(schema_url="/asyncapi",
                      include_in_schema=True, )


def broker():
    return router.broker

@router.get("/")
async def hello_http(broker: Annotated[RabbitBroker, Depends(broker)]):
    await broker.publish("Hello, Rabbit!", "test")
    return "Hello, HTTP!"


def create_app() -> FastAPI:
    container = RegisterContainer()
    db = container.db_container.db()
    db.create_database()
    app = FastAPI(lifespan=router.lifespan_context)
    app.container = container
    app.include_router(wallet_app, tags=["Wallets"])
    app.include_router(auth_app, tags=["Auth"])
    app.include_router(user_app, tags=["User"])
    app.include_router(router, tags=['Propan'])
    return app


app = create_app()


