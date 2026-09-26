import os
import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.main import app

# Import models so Base.metadata registers all tables for create_all().
from src.models import department, employee  # noqa: F401

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "staffsync_test")

TEST_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)
ADMIN_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/mysql"
)


def _ensure_test_database(retries: int = 30) -> None:
    """Wait for MySQL to be reachable and create the test database."""
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            admin_engine = create_engine(ADMIN_DATABASE_URL)
            with admin_engine.connect() as conn:
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS `{TEST_DB_NAME}`")
                )
                conn.commit()
            admin_engine.dispose()
            return
        except OperationalError as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(
        f"Could not connect to MySQL at {DB_HOST}:{DB_PORT}: {last_error}"
    )


@pytest.fixture(scope="session")
def test_engine():
    _ensure_test_database()
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(test_engine):
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()
    try:
        yield session
    finally:
        # Clean all tables (children first) so tests stay isolated.
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
