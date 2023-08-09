from sqlalchemy import *
import datetime

from sqlalchemy.orm import relationship

from src.core.db import Base


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True)
    balance = Column(DECIMAL(precision=10, scale=2))

    asset_id = Column(Integer, ForeignKey('asset.id'))
    asset = relationship("Asset", back_populates="wallets")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="wallets")


class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String)
    image = Column(String, default='str')
    symbol = Column(String)
    decimal_places = Column(DECIMAL())

    blockchain_id = Column(Integer, ForeignKey('blockchain.id'))
    blockchain = relationship("Blockchain", back_populates="wallets")


class Blockchain(Base):
    __tablename__ = 'blockchain'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    image = Column(String, default='str')



