from fastapi import APIRouter, Depends, Query, status
from typing import List
from .. import schemas, crud
from ..database import get_sessionmaker

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, SessionLocal=Depends(get_sessionmaker)):
    with SessionLocal() as db:
        return crud.create_category(db, payload)

@router.get("", response_model=List[schemas.CategoryOut])
def list_categories(user_id: int = Query(...), SessionLocal=Depends(get_sessionmaker)):
    with SessionLocal() as db:
        return crud.list_categories(db, user_id)
