import pytest


@pytest.mark.django_db
def test_successful_loan_application_submission(auth_client, user, loan_payload):
    url = f"/loan/loan-request/{user.id}/"
    response = auth_client.post(url, data=loan_payload, format="json")

    assert response.status_code == 201
    assert response.data["detail"] == "Loan submitted successfully."


@pytest.mark.django_db
def test_fraud_detection_logic(auth_client, user):
    payload = {
        "amount_requested": "10000000.00",  
        "purpose": "Suspiciously large request"
    }

    url = f"/loan/loan-request/{user.id}/"
    response = auth_client.post(url, data=payload, format="json")

    assert response.status_code == 201
    assert response.data["detail"] == "Loan submitted and flagged for review."
    assert "reasons" in response.data
    assert isinstance(response.data["reasons"], list)
    assert any("₦5,000,000" in reason for reason in response.data["reasons"])
