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
