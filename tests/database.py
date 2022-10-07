from sqlalchemy import create_engine
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.testclient import TestClient
import requests 
from app.main import app 
from app.config import settings
from app.database import get_db, Base


#SQLALCHEMY_DATABASE_URL = 'posstgresql://postgres:root@localhot:5432/fastapi_test'

# Database info taken from enviroment variables. Connect to testing DB 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Destroy all tables in DB
    Base.metadata.drop_all(bind=engine)

    # Build tables in DB
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)