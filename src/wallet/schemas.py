from pydantic import BaseModel


class Transaction(BaseModel):
    private_key_sender: str
    receiver_address: str
    value: float


class Wallet(BaseModel):
    wallet_address: str


