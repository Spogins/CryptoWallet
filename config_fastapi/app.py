from typing import Annotated

from asgiref.sync import async_to_sync
from dependency_injector.wiring import Provide, inject
from propan import RabbitBroker

from src.core.db import Database
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
    # db = container.db_container.db()
    # db.create_database()
    app = FastAPI(lifespan=router.lifespan_context)
    app.container = container
    app.include_router(wallet_app, tags=["Wallets"])
    app.include_router(auth_app, tags=["Auth"])
    app.include_router(user_app, tags=["User"])
    app.include_router(router, tags=['Propan'])
    return app

# async def start():
#     container = RegisterContainer()
#     db = container.db_container.db()
#     await db.create_database()
#
# start = start()

app = create_app()


@app.get('/startup')
async def startup():
    print('Create DB')
    container = RegisterContainer()
    db = container.db_container.db()
    await db.create_database()


