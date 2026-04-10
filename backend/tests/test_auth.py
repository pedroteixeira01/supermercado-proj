def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "test@superviva.com", "password": "test1234"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "test@superviva.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_non_existent_user(client):
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "nonexistent@superviva.com", "password": "test1234"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_inactive_user(client, db):
    # Setup an inactive user
    from app.core.security import get_password_hash
    from app.db.models import User

    inactive_user = User(
        email="inactive@superviva.com",
        hashed_password=get_password_hash("test1234"),
        is_active=False,
    )
    db.add(inactive_user)
    db.commit()

    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "inactive@superviva.com", "password": "test1234"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"
