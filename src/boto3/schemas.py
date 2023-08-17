from pydantic import BaseModel


class Base64(BaseModel):
    base64: str
