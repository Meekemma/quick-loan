from django.urls import path
from . import views

urlpatterns = [
    path('loan-request/<uuid:user_id>/', views.loan_request, name='loan_request'),
    path('retrieve-all-loans/<uuid:user_id>/', views.retrieve_all_loans, name='retrieve_all_loans'),
    path('admin/loan/<int:loan_id>/', views.update_loan_status, name='update_loan_status'),
    path('admin/flagged-loans/', views.flagged_loans, name='flagged_loans')

]
