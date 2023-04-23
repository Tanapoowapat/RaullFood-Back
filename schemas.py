from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    email: str
    contact: str

class User(UserBase):
    id: Optional[int] = None
    email: str
    contact: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None