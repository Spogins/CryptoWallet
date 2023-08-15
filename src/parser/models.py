from sqlalchemy import Column, Integer
from src.core.db import Base


class Block(Base):
    __tablename__ = 'block'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, default=4094747)