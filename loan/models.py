from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LoanApplication(models.Model):
    """
    Represents a loan application made by a user.
    """

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2)
    purpose = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_applied = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan {self.amount_requested} by {self.user.get_full_name()} - {self.status}"

    class Meta:
        ordering = ['-date_applied']
        indexes = [
            models.Index(fields=['user']),
        ]


class FraudFlag(models.Model):
    """
    Flags potentially fraudulent loan applications.
    """
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='fraud_flags')
    reason = models.TextField()

    def __str__(self):
        return f"FraudFlag for Loan #{self.loan_application.id} - Reason: {self.reason[:30]}"
