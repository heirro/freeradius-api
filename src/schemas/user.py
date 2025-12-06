from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    value: str
    attribute: str = "Cleartext-Password"
    op: str = ":="


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True 