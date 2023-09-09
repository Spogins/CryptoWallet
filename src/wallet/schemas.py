from pydantic import BaseModel


class Transaction(BaseModel):
    from_address: str
    to_address: str
    value: float


class WalletBalance(BaseModel):
    wallet_address: str


class UserWallet(BaseModel):
    id: int
    address: str
    balance: float
    asset_img: str


class TransForm(BaseModel):
    id: int
    hash: str
    from_address: str
    to_address: str
    value: float
    date: str
    txn_fee: float
    status: str