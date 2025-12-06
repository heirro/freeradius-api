from sqlalchemy import Column, Integer, String
from src.db.database import Base


class RadReply(Base):
    __tablename__ = "radreply"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True)
    attribute = Column(String(64), default="Framed-Pool")
    op = Column(String(2), default=":=")
    value = Column(String(253))
