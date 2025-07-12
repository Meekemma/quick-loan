from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import FraudFlag, LoanApplication

User = get_user_model()


@receiver(post_save, sender=FraudFlag)
def flagged_loan_notification(sender, instance, created, **kwargs):
    if not created:
        return

    loan = instance.loan_application
    user = loan.user

    # Get all reasons for this loan
    reasons = loan.fraud_flags.values_list('reason', flat=True)

    # Get all superuser emails
    superusers = User.objects.filter(is_superuser=True)
    recipient_list = [admin.email for admin in superusers if admin.email]

    if not recipient_list:
        return  

    # Email content
    subject = f"Loan #{loan.id} flagged for fraud"
    context = {
        'loan': loan,
        'user_full_name': user.get_full_name(),
        'user_email': user.email,
        'reasons': reasons,
    }

    html_body = render_to_string('emails/flagged_loan_alert.html', context)
    text_body = render_to_string('emails/flagged_loan_alert.txt', context)
    

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    email.attach_alternative(html_body, "text/html")
    email.send()
