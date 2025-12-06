from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.db.database import Base


class RadUserGroup(Base):
    __tablename__ = "radusergroup"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True)
    groupname = Column(String(64), index=True)
    priority = Column(Integer, default=1) 