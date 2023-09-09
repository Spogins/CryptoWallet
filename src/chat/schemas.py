from typing import Optional, List
from pydantic import BaseModel


class MessageForm(BaseModel):
    text: Optional[str] = ""
    image: Optional[str] = ""


class ChatForm(BaseModel):
    user_id: int
    text: str
    image: Optional[str] = ""
    date: str
    username: str
    user_avatar: str

class UserList(BaseModel):
    users: List[int]