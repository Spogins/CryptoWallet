from dependency_injector.providers import Singleton
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config.settings import URL

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_engine(URL, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()