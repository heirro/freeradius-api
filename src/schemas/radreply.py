from pydantic import BaseModel


class RadReplyBase(BaseModel):
    username: str
    attribute: str
    op: str
    value: str


class RadReplyCreate(RadReplyBase):
    pass


class RadReplySchema(RadReplyBase):
    id: int

    class Config:
        from_attributes = True
