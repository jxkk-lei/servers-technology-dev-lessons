from __future__ import annotations

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product

app = FastAPI(title="Task4 project 9.1")


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: float
    count: int
    description: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductOut])
def list_products(session: Session = Depends(get_db)) -> list[Product]:
    return list(session.scalars(select(Product).order_by(Product.id)))
