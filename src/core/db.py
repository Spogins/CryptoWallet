from dependency_injector.providers import Singleton
from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from config.settings import URL

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_async_engine(URL, echo=True, future=True)
        self._session_factory = async_sessionmaker(self.engine, autoflush=False, expire_on_commit=False)

    async def create_database(self) -> None:
        async with self.engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self._session_factory() as _session:
            try:
                yield _session
            finally:
                await _session.close()
