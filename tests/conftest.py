from typing import Generator

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from api.auth import require_admin
from db import Base, get_db

from api import player, auth, national, club
from models.user import User, RoleEnum

testing_db_url = "sqlite:///:memory:"
engine = create_engine(
    testing_db_url,
    connect_args={"check_same_thread": False}
)
event.listen(
    engine,
    "connect",
    lambda dbapi_connection, _: dbapi_connection.execute("pragma foreign_keys=ON")
)

SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def create_application():
    app = FastAPI()
    app.include_router(player.router)
    app.include_router(auth.router)
    app.include_router(national.router)
    app.include_router(club.router)
    return app

@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, None, None]:
    Base.metadata.create_all(bind=engine)
    _app = create_application()
    yield _app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator[SessionTesting, None, None]:
    connection = engine.connect()
    session = SessionTesting(bind=connection)

    try:
        yield session
    finally:
        session.commit()
        connection.close()
        session.close()

@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, None, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def db():
    db = SessionTesting()
    yield db
    db.close()

@pytest.fixture
def admin_user(db):
    user = User(username="mockadmin", role=RoleEnum.admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def override_admin(app: FastAPI, admin_user):
    def _override():
        try:
            yield admin_user
        finally:
            pass
    app.dependency_overrides[require_admin] = _override
    yield