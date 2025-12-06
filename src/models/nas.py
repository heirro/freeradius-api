from sqlalchemy import Column, Integer, String, Text
from src.db.database import Base


class NAS(Base):
    __tablename__ = "nas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nasname = Column(String(128), index=True)
    shortname = Column(String(32))
    type = Column(String(30), default="other")
    ports = Column(Integer)
    secret = Column(String(60), default="secret")
    server = Column(String(64))
    community = Column(String(50))
    description = Column(String(200), default="RADIUS Client") 