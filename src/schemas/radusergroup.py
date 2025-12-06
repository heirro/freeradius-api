from pydantic import BaseModel
from typing import Optional


class RadUserGroupBase(BaseModel):
    username: str
    groupname: str
    priority: int = 1


class RadUserGroupCreate(RadUserGroupBase):
    pass


class RadUserGroupUpdate(BaseModel):
    groupname: str


class RadUserGroupSchema(RadUserGroupBase):
    id: int

    class Config:
        from_attributes = True 