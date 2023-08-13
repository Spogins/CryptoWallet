from typing import Optional

from pydantic import BaseModel


class MessageForm(BaseModel):
    text: Optional[str] = ""
    image: Optional[str] = ""


class ChatForm(BaseModel):
    id: int
    user_id: int
    text: str
    image: str
    date: str
