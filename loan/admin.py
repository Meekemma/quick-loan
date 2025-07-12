from unfold.admin import ModelAdmin  
from django.contrib import admin
from .models import LoanApplication, FraudFlag


@admin.register(LoanApplication)
class LoanApplicationAdmin(ModelAdmin): 
    list_display = ('id', 'user', 'amount_requested', 'status', 'date_applied')
    list_filter = ('status', 'date_applied')
    search_fields = ('user__username', 'purpose', 'status')
    ordering = ('-date_applied',)
    readonly_fields = ('date_applied', 'date_updated')


@admin.register(FraudFlag)
class FraudFlagAdmin(ModelAdmin): 
    list_display = ('id', 'loan_application', 'reason')
    search_fields = ('reason', 'loan_application__user__first_name')
