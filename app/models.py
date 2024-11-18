from __future__ import annotations

from sqlalchemy import DECIMAL, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class CargoInsurance(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    cargo_date = Column(Date)
    cargos: Mapped[list[Cargo]] = relationship("Cargo", back_populates="insurance")


class Cargo(Base):
    __tablename__ = "cargos"
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String)
    cargo_rate = Column(DECIMAL(10, 2))
    insurance_id = Column(Integer, ForeignKey("uploads.id"))
    insurance = relationship("CargoInsurance", back_populates="cargos")


class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String)
    created_at = Column(Date)
    price = Column(DECIMAL(10, 2))
