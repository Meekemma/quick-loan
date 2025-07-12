from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from .serializers import LoanRequestSerializer
from .models import LoanApplication
from .utils import check_fraud_conditions, flag_loan
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loan_request(request, user_id):
    """
    Allows an authenticated user to apply for a loan.
    Performs fraud checks and flags the loan if suspicious.
    """
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        logger.warning(f"Unauthorized loan attempt by {request.user.email} on behalf of user ID {user_id}")
        return Response({"detail": "You can only apply for a loan on your own behalf."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = LoanRequestSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        loan = serializer.save()

        # Run fraud detection
        reasons = check_fraud_conditions(user, loan.amount_requested)
        if reasons:
            flag_loan(loan, reasons)
            logger.warning(f"Loan #{loan.id} by {user.email} flagged for: {reasons}")
            return Response({
                "detail": "Loan submitted and flagged for review.",
                "reasons": reasons
            }, status=status.HTTP_201_CREATED)

        logger.info(f"Loan #{loan.id} submitted successfully by {user.email}")
        return Response({"detail": "Loan submitted successfully."}, status=status.HTTP_201_CREATED)

    logger.error(f"Loan submission failed for {user.email}: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_all_loans(request, user_id):
    """
    Retrieves all loan applications submitted by the authenticated user.
    """
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        logger.warning(f"Unauthorized loan access attempt by {request.user.email} for user ID {user_id}")
        return Response({"detail": "You can only view your own loans."},
                        status=status.HTTP_403_FORBIDDEN)

    loans = LoanApplication.objects.filter(user=user).order_by('-date_applied')
    paginator = LimitOffsetPagination()
    paginated_loans = paginator.paginate_queryset(loans, request)
    serializer = LoanRequestSerializer(paginated_loans, many=True)

    logger.info(f"{request.user.email} retrieved their loan history")
    return paginator.get_paginated_response(serializer.data)





@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_loan_status(request, loan_id):
    """
    Allows admin to update the status of a loan application.
    """
    loan = get_object_or_404(LoanApplication, id=loan_id)

    serializer = LoanRequestSerializer(instance=loan, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    logger.info(f"Admin {request.user.email} updated Loan #{loan.id} to '{loan.status}'")
    return Response(
        {"detail": f"Loan #{loan.id} status successfully updated to '{loan.status}'"},
        status=status.HTTP_200_OK
    )




@api_view(['GET'])
@permission_classes([IsAdminUser])
def flagged_loans(request):
    """
    Retrieves all loan applications that have been flagged for fraud review.
    """
    loans = LoanApplication.objects.filter(status='flagged').order_by('-date_applied')

    if not loans.exists():
        logger.info("Admin requested flagged loans: none found.")
        return Response(
            {"detail": "No flagged loan applications at this time."},
            status=status.HTTP_200_OK
        )

    paginator = LimitOffsetPagination()
    paginated_loans = paginator.paginate_queryset(loans, request)
    serializer = LoanRequestSerializer(paginated_loans, many=True)

    logger.info(f"Admin {request.user.email} retrieved {len(paginated_loans)} flagged loan(s).")
    return paginator.get_paginated_response(serializer.data)
