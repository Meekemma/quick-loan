import pytest

# Import fixtures from the account app
from account.test.conftest import user as account_user, auth_client as account_auth_client


# Re-expose them under the same names so Pytest can discover them in the loan app's tests
@pytest.fixture
def user(account_user):
    return account_user

@pytest.fixture
def auth_client(account_auth_client):
    return account_auth_client


# Loan-specific fixture
@pytest.fixture
def loan_payload():
    return {
        "amount_requested": "50000.00",
        "purpose": "Business expansion"
    }
