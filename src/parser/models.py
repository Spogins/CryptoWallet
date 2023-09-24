from sqladmin import ModelView
from sqlalchemy import Column, Integer
from src.core.db import Base


class Block(Base):
    __tablename__ = 'block'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=True)


class BlockAdmin(ModelView, model=Block):
    column_list = [
        Block.id,
        Block.number,
    ]