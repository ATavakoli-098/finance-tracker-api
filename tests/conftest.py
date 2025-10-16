# tests/conftest.py
import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_engine, get_sessionmaker


@pytest.fixture(scope="session")
def db_file():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    # final safety cleanup; engine will be disposed before this runs
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def db_url(db_file):
    return f"sqlite:///{db_file}"


@pytest.fixture(scope="session", autouse=True)
def override_db(db_url, db_file):
    # fresh SQLite file for the whole test session
    engine = create_engine(db_url, future=True)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    # create schema
    Base.metadata.create_all(bind=engine)

    # override DI providers
    def _engine():
        return engine

    def _sessionmaker():
        return TestingSessionLocal

    app.dependency_overrides[get_engine] = _engine
    app.dependency_overrides[get_sessionmaker] = _sessionmaker

    yield  # run tests

    # teardown in the right order for Windows
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # release file handles


@pytest.fixture
def client():
    # ensure the client (and its event loop) is closed between tests
    with TestClient(app) as c:
        yield c
