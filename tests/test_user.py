from fastapi import HTTPException
from App import schema , oauth2
import pytest

def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == "Welcome to FastAPI Application"
    assert response.status_code == 200
    print(response.json().get("message"))


def test_create_user(client):
    res = client.post(
        "/users/",
        json={
            "email": "B10TtR@example.com",
            "password": "password123",
            "username": "testuser",
        },
    )
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    user_data = res.json()
    new_user = schema.UserOut(**user_data)
    assert res.json().get("email") == "B10TtR@example.com"
    assert res.status_code == 201

def test_login(client , user):
    res = client.post(
        "/login",
        data={"username": "B10TtR@example.com", "password": "password123"},
    )
    assert res.status_code == 200
    assert res.json().get("token_type") == "bearer"
    assert oauth2.verify_access_token(res.json().get("access_token"), HTTPException(status_code=401, detail="Invalid token"))
    print(f"Login Response: {res.json()}")
    login_res = schema.Token(**res.json())

@pytest.mark.parametrize("email,password,status_code", [
    ("c10TtR@example.com", "wrong_password", 403),
    ("B10TtR@example.com", "wrong_password", 403),
    (None, "wrong_password", 422),
    ("B10TtR@example.com", None, 422),
])
def test_incorrect_login(client,email,password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    print(f"Incorrect Login Response: {res.json()}")
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"