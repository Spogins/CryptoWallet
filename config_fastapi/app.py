from fastapi import FastAPI
from src.core.register import RegisterContainer
from src.users.endpoints import app as user_app
from src.auth.endpoints import app as auth_app


def create_app() -> FastAPI:
    container = RegisterContainer()
    db = container.db_container.db()
    db.create_database()
    app = FastAPI()
    app.container = container
    app.include_router(auth_app, tags=["Auth"])
    app.include_router(user_app, tags=["User"])
    return app


app = create_app()


