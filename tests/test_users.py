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
from app import schemas
from app.config import settings
from app.database import get_db, Base


#SQLALCHEMY_DATABASE_URL = 'posstgresql://postgres:root@localhot:5432/fastapi_test'

# Database info taken from enviroment variables. Connect to testing DB 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency 
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    # Code before 'yield' runs before tests

    # Destroy all tables in DB
    Base.metadata.drop_all(bind=engine)

    # Build tables in DB
    Base.metadata.create_all(bind=engine)
    
    yield TestClient(app)
    # Code after 'yield' runs after tests
    



def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    #print(res.json())

    new_user = schemas.User(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201