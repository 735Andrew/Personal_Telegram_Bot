import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture
def sign_up_url():
    return "http://localhost:8000/users/sign_up"


@pytest.fixture
def sign_up_correct_data():
    return {"login": "@jack", "password": "123456", "name": "Jack"}


@pytest.fixture
def sign_up_incorrect_data_1():
    return {"login": "jack", "password": "123456", "name": "Jack"}


@pytest.fixture
def sign_up_incorrect_data_2():
    return {"login": "@jack", "password": "12", "name": "Jack"}


@pytest.fixture
def sign_up_incorrect_data_3():
    return {"login": "jack", "name": "Jack"}


def test_correct_sign_up(sign_up_url, sign_up_correct_data):
    response = client.post(url=sign_up_url, json=sign_up_correct_data)
    assert response.status_code == 201
    assert str(response.json()["auth_token"]) == "None"
    assert response.json()["login"] == "@jack"
    assert str(response.json()["u_id"]) == "None"
    assert response.json()["name"] == "Jack"


def test_incorrect_sign_up_1(sign_up_url, sign_up_correct_data):
    response = client.post(url=sign_up_url, json=sign_up_correct_data)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "sign_up_incorrect_data",
    [
        sign_up_incorrect_data_1,
        sign_up_incorrect_data_2,
        sign_up_incorrect_data_3,
    ],
)
def test_incorrect_sign_up_2(sign_up_url, sign_up_incorrect_data):
    with pytest.raises(TypeError):
        client.post(url=sign_up_url, json=sign_up_incorrect_data)
