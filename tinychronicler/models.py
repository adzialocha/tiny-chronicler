from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Chronicle(Base):
    __tablename__ = "chronicles"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(255))
    description = Column(Text)

    files = relationship("File", back_populates="chronicle")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    name = Column(String(128))
    path = Column(String(255))
    url = Column(String(255))
    mime = Column(String(64))
    thumb_name = Column(String(128))
    thumb_path = Column(String(255))
    thumb_url = Column(String(255))
    chronicle_id = Column(Integer, ForeignKey("chronicles.id"))

    chronicle = relationship("chronicle", back_populates="files")
