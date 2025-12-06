from pydantic import BaseModel
from typing import Optional


class RadGroupReplyBase(BaseModel):
    groupname: str
    attribute: str
    op: str
    value: str


class RadGroupReplyCreate(RadGroupReplyBase):
    pass


class RadGroupReplySchema(RadGroupReplyBase):
    id: int

    class Config:
        from_attributes = True 