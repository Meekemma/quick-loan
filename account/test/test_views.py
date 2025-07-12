
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_registration_duplicate_email(api_client, user):
    """
    Test that registration fails when using an already registered email.
    The user is provided via the `user` fixture.
    """
    url = "/account/registration/"
    payload = {
        "email": user.email, 
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "AnotherStrong1@",
        "password2": "AnotherStrong1@"
    }

    response = api_client.post(url, data=payload, format="json")

    logger.info(f"Duplicate Email Registration Response: {response.data}")

    assert response.status_code == 400
    assert "email" in response.data






@pytest.mark.django_db
def test_successful_registration(api_client):
    url = "/account/registration/"
    payload = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "NewStrongPass1@",
        "password2": "NewStrongPass1@"
    }

    response = api_client.post(url, data=payload, format="json")

    logger.info(f"Successful Registration Response: {response.data}")

    assert response.status_code == 201
    assert "message" in response.data
    assert response.data["message"] == "Registration successful"







@pytest.mark.django_db
def test_user_login(api_client, login_payload, user):
    url = "/account/login/"
    response = api_client.post(url, data=login_payload, format="json")

    logger.info(f"Login Response Data: {response.data}")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data






