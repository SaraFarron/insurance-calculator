from sqlalchemy import DECIMAL, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    cargo_date = Column(Date)
    cargos = relationship("Cargo", back_populates="upload")


class Cargo(Base):
    __tablename__ = "cargos"
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String)
    cargo_rate = Column(DECIMAL(10, 2))
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    upload = relationship("Upload", back_populates="cargos")


class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String)
    created_at = Column(Date)
    price = Column(DECIMAL(10, 2))
