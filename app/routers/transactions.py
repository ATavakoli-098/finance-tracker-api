from fastapi import APIRouter, Depends, Query, status
from typing import List
from .. import schemas, crud
from ..database import get_sessionmaker

router = APIRouter(prefix="", tags=["transactions"])

@router.post("/transactions", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: schemas.TransactionCreate, SessionLocal=Depends(get_sessionmaker)):
    with SessionLocal() as db:
        return crud.create_transaction(db, payload)

@router.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(user_id: int = Query(...), SessionLocal=Depends(get_sessionmaker)):
    with SessionLocal() as db:
        return crud.list_transactions(db, user_id)

@router.get("/summary")
def get_summary(user_id: int, month: str = Query(..., pattern=r"^\d+$", description="Month (numbers only, e.g. 202510)"), db: Session = Depends(get_db)):
    with SessionLocal() as db:
        return crud.monthly_summary(db, user_id, month)
