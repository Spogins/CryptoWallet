import asyncio
from typing import AsyncIterator
import httpx
import pytest
from fastapi import FastAPI
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.settings import DATABASE_TEST_URL
from src.core.containers import Container, TestContainer
from src.core.db import Base
from src.core.routers import router_app


from src.core.register import RegisterContainer
from src.users.models import User


@pytest.fixture(scope="session", autouse=True)
async def test_db_engine():
    engine = create_async_engine(DATABASE_TEST_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    # await engine.dispose()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




def create_test_app() -> FastAPI:
    container = RegisterContainer()
    test_app = FastAPI()
    test_app.container = container
    test_app.include_router(router_app)
    return test_app


test_app = create_test_app()


@pytest.fixture
def app_test():
    return test_app


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=test_app, base_url="http://testserver") as client:
        yield client



