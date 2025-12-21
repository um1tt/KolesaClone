import pytest
from rest_framework.test import APIClient
from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_success(api_client):
    data = {
        "email": "test@gmail.com",
        "password": "12345678",
        "phone": "87771234567"
    }

    response = api_client.post("/api/auth/register/", data, format="json")

    assert response.status_code == 201
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_register_duplicate_email(api_client):
    User.objects.create_user(email="test@gmail.com", password="12345678")

    response = api_client.post(
        "/api/auth/register/",
        {
            "email": "test@gmail.com",
            "password": "12345678"
        },
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_wrong_password(api_client):
    User.objects.create_user(email="a@gmail.com", password="12345678")

    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "a@gmail.com",
            "password": "wrongpass"
        },
        format="json"
    )

    assert response.status_code == 401
