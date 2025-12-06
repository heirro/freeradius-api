from pydantic import BaseModel
from typing import Optional


class RadGroupCheckBase(BaseModel):
    groupname: str
    attribute: str
    op: str
    value: str


class RadGroupCheckCreate(RadGroupCheckBase):
    pass


class RadGroupCheckSchema(RadGroupCheckBase):
    id: int

    class Config:
        from_attributes = True

