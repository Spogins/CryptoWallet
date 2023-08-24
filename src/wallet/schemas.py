from pydantic import BaseModel


class Transaction(BaseModel):
    private_key_sender: str
    receiver_address: str
    value: float


class WalletBalance(BaseModel):
    wallet_address: str


class UserWallet(BaseModel):
    id: int
    address: str
    balance: float


class TransForm(BaseModel):
    id: int
    hash: str
    from_address: str
    to_address: str
    value: float
    date: str
    txn_fee: float
    status: str