from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.database import Base

class Operator(Base):
    __tablename__ = "operators"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(64))
    firstname = Column(String(64))
    lastname = Column(String(64))
    email = Column(String(64))
    department = Column(String(64))
    company = Column(String(64))
    workphone = Column(String(64))
    homephone = Column(String(64))
    mobilephone = Column(String(64))
    address = Column(String(64))
    city = Column(String(64))
    state = Column(String(64))
    country = Column(String(64))
    zip = Column(String(64))
    notes = Column(String(64))
    enableportallogin = Column(Integer, default=1)
    creationdate = Column(DateTime(timezone=True), server_default=func.now())
    creationby = Column(String(64))
    updatedate = Column(DateTime(timezone=True), onupdate=func.now())
    updateby = Column(String(64)) 