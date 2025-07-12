from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import get_user_model
from .models import LoanApplication, FraudFlag
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


def check_fraud_conditions(user, amount_requested):
    """
    Evaluates multiple fraud criteria for a given loan request.
    Returns a list of reasons if any suspicious activity is detected.
    """
    now = timezone.now()
    reasons = []


    # Condition 1: More than 3 loans submitted by the user in the past 24 hours
    recent_loans = LoanApplication.objects.filter(
        user=user,
        date_applied__gte=now - timedelta(hours=24)
    ).count()
    if recent_loans >= 3:
        reasons.append("More than 3 loans submitted in the last 24 hours.")
        logger.warning(f"Fraud alert for user {user.email}: {recent_loans} loans in 24 hours.")


    # Condition 2: Loan amount exceeds ₦5,000,000
    if amount_requested > 5_000_000:
        reasons.append("Requested amount exceeds ₦5,000,000.")
        logger.warning(f"Fraud alert for user {user.email}: requested ₦{amount_requested:,}.")


    # Condition 3: Email domain shared by more than 10 users
    domain = user.email.split('@')[-1]
    same_domain_count = User.objects.filter(email__iendswith=f"@{domain}").distinct().count()
    if same_domain_count > 10:
        reasons.append(f"Email domain '{domain}' is used by more than 10 users.")
        logger.warning(f"Fraud alert: domain '{domain}' used by {same_domain_count} users.")

    return reasons


def flag_loan(loan, reasons):
    """
    Flags a loan application as suspicious and creates corresponding FraudFlag entries.
    """
    loan.status = 'flagged'
    loan.save()

    for reason in reasons:
        FraudFlag.objects.create(loan_application=loan, reason=reason)
        logger.info(f"Loan #{loan.id} flagged: {reason}")

    logger.info(f"Loan #{loan.id} marked as 'flagged' with {len(reasons)} fraud reason(s).")
