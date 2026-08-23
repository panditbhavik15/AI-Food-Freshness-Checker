"""
Tests for authentication endpoints (register, login, logout, profile).
"""

def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "Password123!",
            "display_name": "New User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == "newuser@example.com"


def test_register_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "weak@example.com",
            "password": "123",
            "display_name": "Weak Pwd",
        },
    )
    # Pydantic validates password min_length=8 at schema level
    assert response.status_code == 422


def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "Password123!",
            "display_name": "Duplicate User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "EMAIL_EXISTS"


def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "WrongPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_get_profile_authenticated(client, auth_headers, test_user):
    response = client.get("/api/v1/auth/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == test_user.email


def test_get_profile_unauthenticated(client):
    response = client.get("/api/v1/auth/profile")
    assert response.status_code == 401
