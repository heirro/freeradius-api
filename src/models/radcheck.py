from sqlalchemy import Column, Integer, String
from src.db.database import Base


class RadCheck(Base):
    __tablename__ = "radcheck"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    attribute = Column(String(64), default="Cleartext-Password")
    op = Column(String(2), default=":=")
    value = Column(String(253)) 