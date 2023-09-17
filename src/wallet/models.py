from sqladmin import ModelView
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from src.core.db import Base


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, index=True)
    private_key = Column(String, unique=True)
    address = Column(String, unique=True)
    balance = Column(DECIMAL, default=0.000000000000000000)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])

    asset_id = Column(Integer, ForeignKey('asset.id'))
    asset = relationship('Asset', foreign_keys=[asset_id])


class WalletAdmin(ModelView, model=Wallet):
    column_list = [
        Wallet.id,
        Wallet.private_key,
        Wallet.address,
        Wallet.balance,
        Wallet.user_id,
        Wallet.user,
        Wallet.asset_id,
        Wallet.asset
    ]


class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String)
    image = Column(URLType, nullable=True)
    symbol = Column(String)
    decimal_places = Column(Integer, default=0)

    blockchain_id = Column(Integer, ForeignKey('blockchain.id'))
    blockchain = relationship('Blockchain', foreign_keys=[blockchain_id])


class AssetAdmin(ModelView, model=Asset):
    column_list = [
        Asset.id,
        Asset.abbreviation,
        Asset.image,
        Asset.symbol,
        Asset.decimal_places,
        Asset.blockchain_id,
        Asset.blockchain
    ]


class Blockchain(Base):
    __tablename__ = 'blockchain'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    image = Column(URLType, nullable=True)


class BlockchainAdmin(ModelView, model=Blockchain):
    column_list = [
        Blockchain.id,
        Blockchain.name,
        Blockchain.code,
        Blockchain.image
    ]


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String)
    from_address = Column(String)
    to_address = Column(String)
    value = Column(DECIMAL)
    date = Column(String, default='PENDING')
    txn_fee = Column(DECIMAL, default=0.0)
    status = Column(String, default='PENDING')


class TransactionAdmin(ModelView, model=Transaction):
    column_list = [
        Transaction.id,
        Transaction.hash,
        Transaction.from_address,
        Transaction.to_address,
        Transaction.value,
        Transaction.date,
        Transaction.txn_fee,
        Transaction.status
    ]







