from pydantic import BaseModel


class NASBase(BaseModel):
    nasname: str
    shortname: str | None = None
    type: str = "other"
    ports: int | None = None
    secret: str = "secret"
    server: str | None = None
    community: str | None = None
    description: str | None = "RADIUS Client"


class NASCreate(NASBase):
    pass


class NAS(NASBase):
    id: int

    class Config:
        from_attributes = True 