# base/test/conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def login_payload():
    return {
        "email": "quickcheck@gmail.com",
        "password": "Testseries1@"
    }


@pytest.fixture
def user(db):
    """
    Creates a test user directly in the DB with verified email.
    """
    password = "Testseries1@"
    user = User.objects.create_user(
        email="quickcheck@gmail.com",
        first_name="Emmanuel",
        last_name="Ibeh",
        password=password
    )
    user.is_verified = True
    user.save()
    return user


@pytest.fixture
def auth_client(user):
    client = APIClient()
    login_data = {
        "email": user.email,
        "password": "Testseries1@"  
    }
    response = client.post("/account/login/", data=login_data, format="json")
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

