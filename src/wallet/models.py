from sqlalchemy import *
import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from src.core.db import Base


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, index=True)
    private_key = Column(String, unique=True)
    address = Column(String, unique=True)
    balance = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    asset_id = Column(Integer, ForeignKey('asset.id'))


class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String)
    image = Column(URLType, nullable=True)
    symbol = Column(String)
    decimal_places = Column(Float, default=0)
    blockchain_id = Column(Integer, ForeignKey('blockchain.id'))
    wallet = relationship('Wallet', backref='asset')


class Blockchain(Base):
    __tablename__ = 'blockchain'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    image = Column(URLType, nullable=True)
    asset = relationship('Asset', backref='blockchain')


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String)
    from_address = Column(String)
    to_address = Column(String)
    value = Column(Float)
    date = Column(String, default='PENDING')
    txn_fee = Column(Float, default=0)
    status = Column(String, default='PENDING')





