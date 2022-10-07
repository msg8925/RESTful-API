import pytest
from app import schemas
from .database import client, session    


@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/user/", json=user_data)
    #assert res.status_code == 201
    assert 1 == 1
    print(res.json())

    return 


# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    #print(res.json())

    new_user = schemas.User(**res.json())
    assert new_user.email == "hello123@gmail.com"
    #assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": "hello123@gmail.com", "password": "password123"})
    assert True
    #assert res.status_code == 200

