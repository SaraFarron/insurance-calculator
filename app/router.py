from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cargo, CargoInsurance, Tariff
from app.schemas import CargoSchema, TariffSchema

router = APIRouter()


@router.post("/tariffs")
async def create_tariff(tariff: TariffSchema, db: Session = Depends(get_db)):
    """Установить новый тариф."""
    new_tariff = Tariff(**tariff.model_dump())
    db.add(new_tariff)
    db.commit()
    return Response(status_code=201)


@router.post("/insurances")
async def create_insurance(insurance: dict[str, list[CargoSchema]], db: Session = Depends(get_db)):
    """Загрузить информацию о грузах для расчетов."""
    for date_str, cargo_insurance_list in insurance.items():
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")  # noqa: DTZ007
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")  # noqa: B904

        db_cargo_insurance = CargoInsurance(
            cargo_date=date,
        )
        for cargo_insurance in cargo_insurance_list:
            db_cargo = Cargo(
                cargo_type=cargo_insurance.cargo_type,
                cargo_rate=cargo_insurance.rate,
            )
            db.add(db_cargo)
        db.add(db_cargo_insurance)
    db.commit()

    return Response(status_code=201)


@router.get("/cargos/{id}")
async def get_insurance(date: str | None = None, cargo_type: str | None = None, db: Session = Depends(get_db)):
    """Посчитать стоимость страхования."""
    latest_tariff = db.query(Tariff).order_by(Tariff.created_at.desc()).first()
    query = (
        db.query(Cargo)
        .join(Cargo.insurance)
        .filter(Cargo.cargo_type == cargo_type, CargoInsurance.cargo_date == date)
        .all()
    )
    total_insurance = sum(cargo.cargo_rate * latest_tariff.price for cargo in query)
    return JSONResponse(content={"total_insurance": total_insurance}, status_code=200)
