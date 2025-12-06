from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RadAcctBase(BaseModel):
    acctsessionid: str
    acctuniqueid: str
    username: str
    realm: Optional[str] = None
    nasipaddress: str
    nasportid: Optional[str] = None
    nasporttype: Optional[str] = None
    acctstarttime: datetime
    acctupdatetime: Optional[datetime] = None
    acctstoptime: Optional[datetime] = None
    acctinterval: Optional[int] = None
    acctsessiontime: Optional[int] = None
    acctauthentic: Optional[str] = None
    connectinfo_start: Optional[str] = None
    connectinfo_stop: Optional[str] = None
    acctinputoctets: Optional[int] = None
    acctoutputoctets: Optional[int] = None
    calledstationid: Optional[str] = None
    callingstationid: Optional[str] = None
    acctterminatecause: Optional[str] = None
    servicetype: Optional[str] = None
    framedprotocol: Optional[str] = None
    framedipaddress: Optional[str] = None

class RadAcctSchema(RadAcctBase):
    radacctid: int

    class Config:
        from_attributes = True 