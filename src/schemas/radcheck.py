from pydantic import BaseModel


class RadCheckBase(BaseModel):
    username: str
    attribute: str
    op: str
    value: str


class RadCheckCreate(RadCheckBase):
    pass


class RadCheckSchema(RadCheckBase):
    id: int

    class Config:
        from_attributes = True
