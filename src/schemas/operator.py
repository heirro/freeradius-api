from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OperatorBase(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class OperatorCreate(OperatorBase):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    company: Optional[str] = None
    workphone: Optional[str] = None
    homephone: Optional[str] = None
    mobilephone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    enableportallogin: Optional[int] = 1

class OperatorSchema(OperatorBase):
    id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    company: Optional[str] = None
    workphone: Optional[str] = None
    homephone: Optional[str] = None
    mobilephone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    enableportallogin: int
    creationdate: datetime
    creationby: Optional[str] = None
    updatedate: Optional[datetime] = None
    updateby: Optional[str] = None

    class Config:
        from_attributes = True 