from fastapi import APIRouter, Depends, status
from .. import schemas, crud
from ..database import get_sessionmaker

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, SessionLocal=Depends(get_sessionmaker)):
    with SessionLocal() as db:
        return crud.create_user(db, payload)
