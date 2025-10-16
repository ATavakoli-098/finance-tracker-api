import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

class Base(DeclarativeBase):
    pass

def get_engine():
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    return create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)

_engine = get_engine()
_SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)

def get_sessionmaker():
    return _SessionLocal
