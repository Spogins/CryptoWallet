from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class DeliveryRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory







