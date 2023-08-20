from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from src.core.db import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)





