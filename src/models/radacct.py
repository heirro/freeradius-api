from sqlalchemy import Column, Integer, String, DateTime, Float
from src.db.database import Base

class RadAcct(Base):
    __tablename__ = "radacct"
    __table_args__ = {'extend_existing': True}

    radacctid = Column(Integer, primary_key=True, index=True)
    acctsessionid = Column(String(64), index=True)
    acctuniqueid = Column(String(32), index=True)
    username = Column(String(64), index=True)
    realm = Column(String(64))
    nasipaddress = Column(String(15), index=True)
    nasportid = Column(String(15))
    nasporttype = Column(String(32))
    acctstarttime = Column(DateTime)
    acctupdatetime = Column(DateTime)
    acctstoptime = Column(DateTime)
    acctinterval = Column(Integer)
    acctsessiontime = Column(Integer)
    acctauthentic = Column(String(32))
    connectinfo_start = Column(String(50))
    connectinfo_stop = Column(String(50))
    acctinputoctets = Column(Integer)
    acctoutputoctets = Column(Integer)
    calledstationid = Column(String(50))
    callingstationid = Column(String(50))
    acctterminatecause = Column(String(32))
    servicetype = Column(String(32))
    framedprotocol = Column(String(32))
    framedipaddress = Column(String(15)) 