from sqlalchemy import Column, Integer, String
from src.db.database import Base


class RadGroupReply(Base):
    __tablename__ = "radgroupreply"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String(64), index=True)
    attribute = Column(String(64))
    op = Column(String(2), default=":=")
    value = Column(String(253)) 