from typing import Callable, Iterator
from sqlalchemy.orm import Session


class WalletRepository:
    def __init__(self, session_factory: Callable[..., Session]) -> None:
        self.session_factory = session_factory
